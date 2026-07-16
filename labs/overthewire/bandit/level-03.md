# OverTheWire - Bandit: Nivel 03 → 04 - Archivos ocultos (dotfiles)

## Comando(s)

```bash
ls -la
```
```bash
cd inhere
```
```bash
ls -la
```
```bash
cat ./...Hiding-From-You
```

## Concepto

Los archivos que empiezan con `.` son ocultos y `ls` normal no los muestra.

## Aplicación real

Encontrar configuraciones, historiales, claves y archivos ocultos en home directories.

## Errores comunes

- Usar `ls` sin `-la` y no ver el archivo.
- No saber que el punto puede preceder a un nombre largo.

## Variantes útiles

- `ls -la` muestra todo incluyendo `.` y `..`.
- `find . -name '.*' -type f` encuentra dotfiles.
