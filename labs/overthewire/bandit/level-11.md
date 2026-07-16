# OverTheWire - Bandit: Nivel 11 → 12 - ROT13 con `tr`

## Comando(s)

```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

## Concepto

ROT13 es una sustitución cíclica de 13 posiciones. `tr` mapea rangos de caracteres.

## Aplicación real

Ofuscación simple en CTFs, malware y payloads. No es cifrado seguro.

## Errores comunes

- No incluir tanto mayúsculas como minúsculas en el mapeo.
- Pensar que ROT13 es criptografía fuerte.

## Variantes útiles

- Para ROT13 aplicado dos veces vuelve al texto original.
- `tr 'A-Za-z' 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'` equivalente.
