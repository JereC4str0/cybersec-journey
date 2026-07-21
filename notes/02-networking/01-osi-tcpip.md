# 01 — OSI / TCP-IP y el three-way handshake

> Sesión 002 — Bloque 02 Networking. Material de repaso.
> Referencia: The TCP/IP Guide (tcpipguide.com), Nmap Reference Guide.

## Concepto: handshake de 3 vías

TCP es orientado a conexión: antes de mandar datos, las dos partes negocian
la apertura con 3 paquetes:

1. **SYN** — el cliente propone la conexión e informa su número de secuencia
   inicial (ISN). Ej: `seq 307277771`.
2. **SYN-ACK** — el servidor acepta, manda su propio ISN y confirma el del
   cliente con `ack = ISN_cliente + 1` (el SYN consume un número de secuencia).
3. **ACK** — el cliente confirma. Conexión establecida, fluyen datos.

Flags relevantes:
- `SYN` — iniciar conexión.
- `ACK` — confirmar recepción.
- `RST` — reset: "no hay nadie" o "cerrá esto ya".
- `FIN` — cierre ordenado.

## Por qué importa para pentesting

Los estados de puerto de Nmap se deducen de cómo responde el objetivo
al handshake:

| Respuesta al SYN | Estado Nmap | Significado |
|---|---|---|
| SYN-ACK | `open` | hay un servicio escuchando |
| RST | `closed` | el host responde pero nadie escucha en ese puerto |
| silencio / timeout | `filtered` | un firewall descarta el paquete |
| ICMP unreachable | `filtered` | un firewall rechaza activamente |

## Las 3 firmas de escaneo (capturadas en lab propio)

### Puerto abierto + connect scan (`-sT`)
Handshake completo vía kernel, luego RST de cierre:
```
[S]  cliente → servidor
[S.] servidor → cliente
[.]  cliente → servidor   ← handshake completo
[R.] cliente → servidor   ← Nmap cierra de golpe
```

### Puerto cerrado
```
[S]  cliente → servidor
[R.] servidor → cliente   ← RST seco: puerto cerrado
```

### Puerto abierto + SYN scan (`-sS`) — "half-open"
```
[S]  cliente → servidor   ← paquete crudo de Nmap (firma: win 1024, mss 1460)
[S.] servidor → cliente
[R]  cliente → servidor   ← RST en lugar del ACK final
```

**Por qué el tercer paquete es RST:** Nmap inyecta el SYN crudo sin usar
`connect()`. Cuando vuelve el SYN-ACK, el kernel local no tiene registro de
esa conexión y responde RST por su cuenta. La conexión nunca se completa:
la aplicación que escucha no llega a registrarla en sus logs.

## Detección (mirada blue team)

- Un SYN scan es distinguible del tráfico real por las opciones TCP:
  - SYN de kernel (`connect()`): `win` grande, `sackOK`, `TS`, `wscale`.
  - SYN crudo de Nmap: `win 1024`, `mss 1460`, sin timestamps.
- "Half-open" evita logs de la aplicación, NO evita IDS/firewall.
- Un burst de SYNs a miles de puertos en segundos es ruidoso de todas formas.

## Errores comunes

- Creer que `filtered` = puerto cerrado. Cerrado responde RST; filtrado no
  responde nada.
- Confiar en un solo escaneo: el estado del objetivo cambia (en el lab, el
  listener `nc` sin `-k` murió tras la primera conexión y el segundo escaneo
  reportó el puerto cerrado). Re-verificar antes de reportar.
- Olvidar que escanear requiere root para `-sS` (raw sockets); sin root,
  Nmap cae en `-sT` silenciosamente.

## Autoevaluación

1. Si el SYN-ACK lleva `ack 5001`, ¿cuál era el ISN del cliente?
2. ¿Qué diferencia hay entre `[R]` y `[R.]`?
3. ¿Por qué un firewall que descarta paquetes hace más lento el escaneo
   que uno que responde RST?
4. ¿Quién envía el RST final en un SYN scan y por qué?
