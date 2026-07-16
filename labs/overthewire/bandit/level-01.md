# OverTheWire - Bandit: Nivel 01 → 02 - Archivos con nombre `-`

## Comando(s)

```bash
cat ./-
```
```bash
cat -- -
```

## Concepto

El shell puede confundir un guion al inicio del nombre con una opción/flag del comando.

## Aplicación real

Trabajar con archivos maliciosos o nombres inusuales que rompen scripts mal escritos.

## Errores comunes

- `cat -` lee de stdin en lugar del archivo.
- No usar `--` para terminar opciones.

## Variantes útiles

- `./-` fuerza a tratarlo como archivo.
- `cat -- archivo` indica fin de opciones.
