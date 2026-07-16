# OverTheWire - Bandit: Resumen completo Niveles 0 → 32

## Introducción

Bandit es una serie de wargames de OverTheWire orientada a practicar comandos Linux, reconocimiento básico, manipulación de datos, networking, escalada de privilegios, Git y escapes de shell. Esta carpeta contiene writeups individuales de cada nivel y este resumen general.

## Reglas de documentación

- **No se incluyen contraseñas ni claves privadas** en el repositorio.
- Cada writeup sigue el formato: comando(s), concepto, aplicación real, errores comunes, variantes útiles.
- Este README es el resumen completo para repaso rápido.

## Resumen de niveles

| Nivel | Tema | Comandos clave | Concepto central |
|-------|------|----------------|------------------|
| 00 → 01 | SSH, ls, cat | `ssh -p 2220 bandit0@...`, `ls`, `cat` | Acceso remoto por SSH y lectura de archivos. |
| 01 → 02 | Archivos con nombre especial | `cat ./-` | Nombres que empiezan con `-` se interpretan como flags. |
| 02 → 03 | Espacios y guiones | `cat "spaces in this filename"` | Uso de comillas para nombres con espacios. |
| 03 → 04 | Archivos ocultos | `ls -la`, `cat ...Hiding-From-You` | Los dotfiles no aparecen en `ls` normal. |
| 04 → 05 | Identificar tipo de archivo | `file ./*` | `file` detecta el tipo de archivo por su contenido. |
| 05 → 06 | Filtrar archivos con find | `find -size`, `-perm`, `-user` | `find` permite búsquedas por tamaño, permisos y propietario. |
| 06 → 07 | Buscar en todo el sistema | `find / -size 33c -group bandit6 -user bandit7 2>/dev/null` | Redirigir errores para limpiar output. |
| 07 → 08 | Filtrar con grep | `grep millionth data.txt` | Buscar patrones en archivos grandes. |
| 08 → 09 | Líneas únicas | `sort data.txt | uniq -u` | Encontrar la línea que aparece una sola vez. |
| 09 → 10 | Extraer strings de binarios | `strings data.txt | grep ^=` | `strings` muestra texto legible en binarios. |
| 10 → 11 | Base64 | `base64 -d data.txt` | Decodificación de datos en base64. |
| 11 → 12 | ROT13 | `cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'` | Rotación de caracteres con `tr`. |
| 12 → 13 | Compresión anidada | `xxd`, `gzip`, `bzip2`, `tar` | Desempaquetado iterativo de archivos comprimidos. |
| 13 → 14 | SSH con clave privada | `ssh -i sshkey.private ...` | Autenticación por clave en lugar de password. |
| 14 → 15 | Netcat | `nc localhost 30000`, `echo password | nc ...` | Envío de datos por TCP. |
| 15 → 16 | SSL/TLS | `openssl s_client -connect localhost:30001 -ign_eof` | Conexión cifrada con OpenSSL. |
| 16 → 17 | Escaneo de puertos y servicios | `nmap -p 31000-32000 localhost`, `openssl s_client -connect` | Encontrar servicios SSL que aceptan el password. |
| 17 → 18 | Comparar archivos | `diff passwords.new passwords.old` | Detectar cambios entre versiones. |
| 18 → 19 | Ejecución remota sin shell | `ssh user@host "cat readme"` | Bypass de shells que se cierran al inicio. |
| 19 → 20 | Binarios setuid | `./bandit20-do cat ...` | Ejecutar con privilegios del propietario. |
| 20 → 21 | Listener + setuid | `cat pass | nc -l -p 12345 & ./suconnect 12345` | Comunicación local para validar credenciales. |
| 21 → 22 | Cron jobs | `cat /etc/cron.d/cronjob_bandit22`, leer script | Tareas programadas que ejecutan scripts como otro usuario. |
| 22 → 23 | Cron con hash dinámico | `echo "I am user bandit23" | md5sum | cut -d ' ' -f 1` | Reproducir cálculo del script para hallar archivo. |
| 23 → 24 | Escalada via cron y directorio escribible | escribir script en spool, `chmod +x`, esperar cron | Ejecutar código como usuario privilegiado a través de cron. |
| 24 → 25 | Fuerza bruta de PIN | `for i in {0000..9999}; do echo ...; done | nc ...` | Enumeración de códigos cortos. |
| 25 → 26 | Escape desde more/vim | `stty rows 5 cols 80`, `ssh -i key -t ...`, `v`, `:set shell=/bin/bash`, `:shell` | Escapar de shell forzado usando paginador/editor. |
| 26 → 27 | Setuid | `./bandit27-do cat ...` | Binario setuid para leer archivos protegidos. |
| 27 → 28 | Git clone | `git clone ssh://bandit27-git@...` | Password expuesto en archivo de repo. |
| 28 → 29 | Git history | `git log`, `git show <hash>` | Password en commit anterior. |
| 29 → 30 | Git branches | `git branch -a`, `git checkout remotes/origin/dev` | Password en rama de desarrollo. |
| 30 → 31 | Git tags | `git tag`, `git show <tag>` | Password en tag. |
| 31 → 32 | Git hooks + `.gitignore` | `echo "..." > key.txt`, `git add -f`, `git push` | Bypass de `.gitignore` y validación en servidor. |
| 32 → 33 | Escape de shell | `$0`, `cat /etc/bandit_pass/bandit33` | Wrapper de shell bypassado con `$0`. |

## Lecciones principales

1. **Reconocimiento de archivos**: `ls -la`, `file`, `find`, `strings` y `grep` son la base.
2. **Codificación y compresión**: base64, ROT13, gzip/bzip2/tar anidados.
3. **Networking**: netcat, OpenSSL, nmap, SSH con clave.
4. **Privilegios**: setuid, cron jobs, directorios escribibles por usuarios privilegiados.
5. **Fuerza bruta**: PINs y códigos cortos son vulnerables sin rate limiting.
6. **Escapes de shell**: paginadores, editores y variables como `$0`.
7. **Git**: historial, ramas, tags, `.gitignore` y hooks pueden filtrar o ejecutar lógica sensible.

## Aplicación ofensiva

- Buscar secrets en repos Git (historial, ramas, tags).
- Aprovechar binarios setuid y cron mal configurados para escalar.
- Escapar de shells restringidos en jaulas, contenedores o cuentas limitadas.
- Realizar fuerza bruta a PINs, logins y códigos de verificación.
- Usar paginadores/editores como vectores de escape.

## Defensa recomendada

- No hardcodear secrets; usar gestores de secretos y rotar credenciales.
- Revisar permisos de setuid, cron jobs y directorios escribibles.
- Proteger ramas principales, usar hooks `pre-receive` y escanear repos con `truffleHog`/`gitleaks`.
- Limitar shells forzados y usar `ForceCommand` con cuidado.
- Implementar rate limiting, captchas y 2FA para mitigar fuerza bruta.

## Errores comunes

- No usar `ls -la` y perderse archivos ocultos.
- Confundirse con nombres de archivo que empiezan con `-`.
- No redirigir errores de `find` con `2>/dev/null`.
- Olvidar `chmod +x` en scripts de cron.
- No usar `-t` en SSH cuando se necesita pseudo-terminal.
- Depender de `.gitignore` como barrera de seguridad.
- No revisar historial, ramas y tags en audits de Git.

## Variantes útiles

- `find / -type f -size 33c 2>/dev/null`
- `strings -n 8 archivo | grep patron`
- `base64 -d`, `tr 'A-Za-z' 'N-ZA-Mn-za-m'`
- `xxd`, `gzip -d`, `bzip2 -d`, `tar -xvf`
- `ssh -i key -t user@host comando`
- `openssl s_client -connect host:puerto -ign_eof`
- `nmap -p rango -sV localhost`
- `diff -u archivo1 archivo2`
- `find / -perm -4000 -type f 2>/dev/null`
- `crontab -l`, `ls -la /etc/cron.d/`, `cat /etc/crontab`
- `git log --all --oneline`, `git branch -a`, `git tag`, `git show <hash>`
- `$0`, `$SHELL`, `bash -i`, `python3 -c 'import pty; pty.spawn("/bin/bash")'`

## Recursos útiles

- https://overthewire.org/wargames/bandit/
- https://explainshell.com/
- https://gtfobins.github.io/
