# OverTheWire - Bandit: Nivel 21 → 22 - Cron jobs

## Comando(s)

```bash
ls /etc/cron.d/
```
```bash
cat /etc/cron.d/cronjob_bandit22
```
```bash
cat /usr/bin/cronjob_bandit22.sh
```
```bash
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

## Concepto

`cron` es el planificador de tareas de Linux. El archivo `/etc/cron.d/cronjob_bandit22` define que el script `/usr/bin/cronjob_bandit22.sh` se ejecuta cada minuto como el usuario `bandit22`. El script copia el password de `bandit22` a un archivo en `/tmp`.

## Aplicación real

- **Persistencia**: atacantes dejan cron jobs para ejecutar backdoors periódicamente.
- **Credential leaks**: scripts de cron que escriben secrets en archivos temporales o logs.
- **Escalada de privilegios**: un script de cron ejecutado por root que puede ser modificado permite escalar.

## Errores comunes

- No revisar `/etc/cron.d/` y `/etc/crontab`.
- No leer el script apuntado por el cron job.
- Ignorar que cron jobs ejecutan como otro usuario, con sus permisos.

## Variantes útiles

- `crontab -l` lista los cron jobs del usuario actual.
- `/etc/crontab` cron jobs globales del sistema.
- `/var/spool/cron/crontabs/` jobs de usuarios.
- `ls -la /etc/cron.*` verifica directorios de cron diario/semanal/mensual.
- `grep -r "bandit" /etc/cron*` busca jobs relacionados con un usuario.
