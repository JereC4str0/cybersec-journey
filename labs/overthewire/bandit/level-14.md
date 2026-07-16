# OverTheWire - Bandit: Nivel 14 → 15 - Enviar datos con `nc` (netcat)

## Comando(s)

```bash
cat /etc/bandit_pass/bandit14 | nc localhost 30000
```
```bash
nc localhost 30000
```

## Concepto

`nc` abre conexiones TCP. Con el pipe podemos enviar contenido de archivos a servicios.

## Aplicación real

Prueba de servicios, banners grabbing, exfiltración simple y reverse shells.

## Errores comunes

- Usar el puerto equivocado (3000 en lugar de 30000).
- No incluir el pipe y enviar el archivo entero como argumento.

## Variantes útiles

- `nc -zv host port` verifica si puerto abierto.
- `nc -l -p 1234` escucha en un puerto.
