# OverTheWire - Bandit: Nivel 07 → 08 - Filtrar líneas con `grep`

## Comando(s)

```bash
grep 'millionth' data.txt
```

## Concepto

`grep` busca patrones en archivos y muestra líneas coincidentes.

## Aplicación real

Búsqueda de strings, credenciales, IPs, flags y errores en logs y archivos grandes.

## Errores comunes

- Buscar con mayúsculas/minúsculas sin `-i`.
- No escapar caracteres especiales en el patrón.

## Variantes útiles

- `grep -i` case insensitive.
- `grep -v` líneas que NO coinciden.
- `grep -n` muestra número de línea.
