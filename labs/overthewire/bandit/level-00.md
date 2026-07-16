# OverTheWire - Bandit: Nivel 00 → 01 - SSH, ls y cat

## Comando(s)

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```
```bash
ls
```
```bash
cat readme
```

## Concepto

Conexión SSH en puerto no estándar y lectura básica de archivos.

## Aplicación real

Acceso remoto a servidores y enumeración rápida de archivos tras conseguir shell.

## Errores comunes

- Olvidar el puerto 2220.
- Confundirse entre login, shell local y shell remoto.

## Variantes útiles

- `ssh -p 2220 usuario@host` (el `-p` va antes de `-p` del puerto; para scp es `-P`).
- `ls -la` para ver archivos ocultos.
