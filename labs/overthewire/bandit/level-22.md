# OverTheWire - Bandit: Nivel 22 → 23 - Cron job con hash dinámico

## Comando(s)

```bash
cat /etc/cron.d/cronjob_bandit23
```
```bash
cat /usr/bin/cronjob_bandit23.sh
```
```bash
echo "I am user bandit23" | md5sum | cut -d ' ' -f 1
```
```bash
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

## Concepto

El cron job ejecuta un script como `bandit23`. El script calcula el nombre del archivo destino usando el hash MD5 de una cadena que incluye el nombre de usuario. Como conocemos el usuario (`bandit23`), podemos reproducir el cálculo y leer el archivo.

## Aplicación real

- **Ofuscación débil**: programadores que creen que un nombre de archivo basado en hash es secreto.
- **Reversing de scripts**: entender cómo un script genera rutas o nombres para predecir dónde escriben datos.
- **Cron jobs maliciosos**: scripts que generan nombres pseudoaleatorios para ocultar exfiltración.

## Errores comunes

- No leer el script y asumir que el archivo destino es fijo.
- No replicar exactamente el comando del script (espacios, orden de palabras).
- Usar un algoritmo de hash diferente.

## Variantes útiles

- `echo "cadena" | md5sum` calcula MD5.
- `echo "cadena" | sha256sum` calcula SHA-256.
- `cut -d ' ' -f 1` extrae solo el hash sin el guion.
- `echo -n "cadena" | md5sum` evita el salto de línea.
- `md5sum <<< "cadena"` alternativa desde bash.
