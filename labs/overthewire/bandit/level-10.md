# OverTheWire - Bandit: Nivel 10 → 11 - Decodificar base64

## Comando(s)

```bash
base64 -d data.txt
```

## Concepto

`base64 -d` decodifica datos en base64.

## Aplicación real

Decodificar tokens, headers, payloads HTTP y datos ofuscados en aplicaciones web.

## Errores comunes

- Usar `base64` sin `-d` y codificar dos veces.
- No notar que base64 a veces está url-encoded.

## Variantes útiles

- `echo '...' | base64 -d`.
- `base64 -w 0 archivo` para codificar sin saltos de línea.
