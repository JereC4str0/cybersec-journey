# OverTheWire - Bandit: Nivel 32 → 33 - Shell restringido

## Comando(s)

Conectar:
```bash
ssh bandit32@bandit.labs.overthewire.org -p 2220
```

Dentro del shell restringido:
```bash
$0
ls
whoami
cat /etc/bandit_pass/bandit33
exit
```

## Concepto

El shell asignado convierte todos los comandos a mayúsculas antes de ejecutarlos, por lo que comandos como `bash` se convierten en `BASH` y fallan. La variable `$0` representa el nombre del intérprete que está ejecutando el script o la shell actual. Al invocar `$0`, se inicia una shell sin el wrapper restringido, dando acceso a una shell normal.

## Aplicación real

- **Escape de shells restringidos**: `rbash`, `rksh`, `chroot` o shells personalizados que limitan comandos.
- **Escalada de privilegios**: contenedores, jaulas o cuentas de servicio con shells limitados.
- **Defensa**: no usar wrappers triviales como conversión a mayúsculas como control de seguridad; usar `rbash` bien configurado, chroot con privaciones, o SELinux/AppArmor.

## Errores comunes

- Escribir comandos directamente en mayúsculas sin entender que el shell los transforma.
- No probar variables del entorno como `$0` para escapar del wrapper.
- Intentar salir con `exit` estando aún dentro del shell restringido.

## Variantes útiles

- `$0` invoca la shell actual sin el wrapper.
- `$SHELL` puede apuntar a `/bin/bash` u otro intérprete.
- `bash -i` fuerza una shell interactiva si `bash` está disponible.
- `python3 -c 'import pty; pty.spawn("/bin/bash")'` para obtener una TTY completa.
- `vi`, `less`, `man` u otros paginadores pueden lanzar shells con `!bash` o `!sh`.
- `awk 'BEGIN {system("/bin/bash")}'` ejecuta comandos desde un binario con SUID o en entornos limitados.
