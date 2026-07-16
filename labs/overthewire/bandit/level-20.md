# OverTheWire - Bandit: Nivel 20 → 21 - Listener con netcat y binario setuid

## Comando(s)

```bash
cat /etc/bandit_pass/bandit20 | nc -l -p 12345 & ./suconnect 12345
```

## Concepto

`suconnect` es un binario setuid propiedad de `bandit21` que se conecta a un puerto TCP local. El atacante levanta un listener con `nc` que envía el password de `bandit20`. `suconnect` valida el password y devuelve el password de `bandit21`.

## Aplicación real

- **Bind shells**: un listener espera conexiones para ejecutar comandos.
- **Comunicación entre procesos** en un mismo host usando TCP.
- **Exfiltración** a través de binarios legítimos que conectan a un listener controlado.
- **Background jobs**: el `&` permite ejecutar procesos sin bloquear la terminal.

## Errores comunes

- No usar `&` y quedar bloqueado en el listener.
- Elegir un puerto bajo (&lt;1024) sin permisos de root.
- Usar netcat de una versión incompatible.
- No entender que el listener debe enviar el password antes de que suconnect lo solicite.

## Variantes útiles

- `nc -l -p 1234` escucha en el puerto 1234.
- `nc -lvp 1234` escucha en modo verbose (algunas versiones).
- `cat archivo | nc host puerto` envía el contenido de un archivo.
- `nc -l -p 1234 -e /bin/bash` bind shell (no suele estar habilitado en netcat moderno).
- `nohup comando &` para que el proceso sobreviva al cierre de la terminal.
