# OverTheWire - Bandit: Nivel 15 → 16 - Conexiones SSL/TLS con `openssl s_client`

## Comando(s)

```bash
cat /etc/bandit_pass/bandit15 | openssl s_client -connect localhost:30001 -ign_eof
```

## Concepto

`openssl s_client` es un cliente TLS para probar servicios encriptados. `-ign_eof` mantiene la conexión abierta.

## Aplicación real

Inspección de certificados, prueba de APIs SSL, análisis de servicios encriptados internos.

## Errores comunes

- Olvidar `-ign_eof` y cerrar la conexión antes de recibir respuesta.
- Asustarse con 'self-signed certificate' en entornos de lab.

## Variantes útiles

- `openssl s_client -connect host:port` para ver certificado.
- `openssl s_client -showcerts` muestra toda la cadena.
