# OverTheWire - Bandit: Nivel 02 → 03 - Espacios y guiones en nombres de archivo

## Comando(s)

```bash
cat -- "--spaces in this filename--"
```
```bash
cat -- '--spaces in this filename--'
```
```bash
cat -- --spaces\ in\ this\ filename--
```

## Concepto

Combinación de espacios y guiones en nombres. Se resuelve con comillas o escapes más `--`.

## Aplicación real

Manejo de archivos con nombres que incluyen espacios y caracteres especiales en pentests y forense.

## Errores comunes

- Escapar espacios dentro de comillas dobles.
- Dejar un backslash al final del comando.

## Variantes útiles

- Comillas simples: `'archivo con espacios'`.
- Comillas dobles: `"archivo con espacios"`.
