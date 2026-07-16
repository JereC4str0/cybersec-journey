# OverTheWire - Bandit: Nivel 16 → 17 - Escaneo de puertos con `nmap` y servicios SSL

## Comando(s)

```bash
nmap -p 31000-32000 -sV localhost
```
```bash
cat /etc/bandit_pass/bandit16 | openssl s_client -connect localhost:31790 -ign_eof
```

## Concepto

Escaneo de puertos locales para encontrar servicios ocultos. Identificación de puerto SSL por `nmap` y fingerprinting.

## Aplicación real

Reconocimiento interno post-explotación: encontrar servicios localhost no expuestos externamente.

## Errores comunes

- Conectar al puerto equivocado (ssl/echo en lugar de ssl/unknown).
- No interpretar el fingerprint de `nmap`.

## Variantes útiles

- `nmap -p- host` escanea todos los puertos.
- `nmap -sV -sC` detección de servicios y scripts por defecto.
