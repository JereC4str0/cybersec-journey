# OverTheWire - Bandit: Nivel 18 → 19 - Ejecución remota sin shell interactivo

## Comando(s)

```bash
ssh -p 2220 bandit18@bandit.labs.overthewire.org "cat readme"
```

## Concepto

SSH permite ejecutar un comando remoto directamente sin abrir un shell interactivo. Esto bypassear configuraciones del shell que cierran la sesión al iniciar (como `exit` en `.bashrc` o `.bash_profile`).

## Aplicación real

- Automatización de tareas en servidores remotos.
- Bypassear shells restringidas o forzadas.
- Ejecutar comandos en sistemas donde no se puede obtener shell interactivo.
- Lateral movement cuando se tiene acceso SSH pero el entorno limita interacción.

## Errores comunes

- No usar comillas y que el shell local interprete parte del comando.
- Pensar que sin shell no se puede ejecutar nada.
- Olvidar que el comando se ejecuta en el contexto del usuario remoto.

## Variantes útiles

- `ssh user@host "ls -la"` ejecuta un comando.
- `ssh user@host 'cd /tmp && ls'` combina múltiples comandos.
- `ssh user@host /bin/bash` intenta abrir un shell específico.
- `ssh user@host "cat /etc/passwd"` lectura directa de archivos del sistema.
