# OverTheWire - Bandit: Nivel 09 → 10 - Extraer strings de binarios

## Comando(s)

```bash
strings data.txt | grep '='
```

## Concepto

`strings` extrae cadenas legibles de archivos binarios.

## Aplicación real

Análisis de malware, ejecutables, dumps de memoria y firmware para encontrar secrets.

## Errores comunes

- No filtrar con grep y perderse en cientos de líneas.
- Asumir que el string importante está al principio.

## Variantes útiles

- `strings -n 8` strings de mínimo 8 caracteres.
- `strings -e l` codificación UTF-16LE (Windows).
