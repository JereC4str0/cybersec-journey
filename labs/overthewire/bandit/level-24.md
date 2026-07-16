# OverTheWire - Bandit: Nivel 24 → 25 - Fuerza bruta de PIN

## Comando(s)

```bash
for i in {0000..9999}; do echo "PASSWORD_DE_BANDIT24 $i"; done | nc localhost 30002
```

## Concepto

El servicio en `localhost:30002` requiere el password de `bandit24` más un PIN de 4 dígitos. Como el PIN solo tiene 4 dígitos, existen 10000 combinaciones posibles. Un loop genera todas las combinaciones y las envía a través de `nc` hasta que el servicio responde "Correct".

## Aplicación real

- Ataques de fuerza bruta a PINs, códigos de verificación y contraseñas débiles.
- En pentesting web: brute force de login con herramientas como Hydra, Burp Intruder o scripts personalizados.
- Sistemas reales usan rate limiting, bloqueo de cuentas, captchas y 2FA para mitigar este tipo de ataques.

## Errores comunes

- Olvidar el password de `bandit24` al inicio de cada línea.
- No esperar a que el servicio procese todas las combinaciones.
- Si el servicio cierra conexiones por intento, enviar todo en una sola conexión no funciona.

## Variantes útiles

- Loop con conexiones separadas: `for i in {0000..9999}; do echo "password $i" | nc -q 1 localhost 30002; done | grep -v "Wrong"`.
- Script en Python con sockets para controlar timeouts y respuestas.
- Hydra: `hydra -l user -P wordlist target http-post-form`.
- Generar wordlist: `crunch 4 4 0123456789`.
- Filtrar respuestas: `... | grep -v "Wrong"`.
