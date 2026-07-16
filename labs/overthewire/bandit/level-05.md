# OverTheWire - Bandit: Nivel 05 → 06 - Filtrar archivos con `find`

## Comando(s)

```bash
cd inhere
```
```bash
find . -type f -size 1033c ! -executable
```
```bash
cat ./maybehere07/.file2
```

## Concepto

`find` permite buscar archivos por tipo, tamaño y permisos.

## Aplicación real

Búsqueda de archivos sospechosos, logs, backups o secretos en sistemas comprometidos.

## Errores comunes

- Confundir `c` (bytes) con `k` (kilobytes) en `-size`.
- No usar `-type f` y que devuelva directorios.

## Variantes útiles

- `find / -type f -size +10M` archivos grandes.
- `find . -perm -4000` archivos SUID.
