# 03 — Captura del handshake con tcpdump (lab)

> Sesión 002 — Bloque 02 Networking. Evidencia de laboratorio propio.
> Setup: `nc -k -l -p 22222` como servicio de prueba en localhost;
> captura con `sudo tcpdump -i lo -n 'tcp port 22222'`.

## Comandos del lab

```bash
# Terminal 1 — captura en loopback
sudo tcpdump -i lo -n 'tcp port 22222'

# Terminal 2 — listener persistente (-k = no morir tras la 1ra conexión)
nc -k -l -p 22222 &

# Escaneos
nmap -sT -p 22222 localhost        # connect scan (no requiere root)
sudo nmap -sS -p 22222 localhost   # SYN scan (raw sockets, requiere root)
```

## Captura 1 — connect scan (`-sT`), puerto abierto

```
06:46:00.992908 IP 127.0.0.1.35974 > 127.0.0.1.22222: Flags [S], seq 3438309496, win 65495, options [mss 65495,sackOK,TS val 3762542832 ecr 0,nop,wscale 10], length 0
06:46:00.992936 IP 127.0.0.1.22222 > 127.0.0.1.35974: Flags [S.], seq 3642625075, ack 3438309497, win 65483, options [mss 65495,sackOK,TS val 1800222955 ecr 3762542832,nop,wscale 10], length 0
06:46:00.992944 IP 127.0.0.1.35974 > 127.0.0.1.22222: Flags [.], ack 1, win 64, options [nop,nop,TS val 3762542832 ecr 1800222955], length 0
06:46:00.992960 IP 127.0.0.1.35974 > 127.0.0.1.22222: Flags [R.], seq 1, ack 1, win 64, options [nop,nop,TS val 3762542832 ecr 1800222955], length 0
```

Lectura línea por línea:
1. `SYN` con ISN 3438309496. Opciones ricas (sackOK, TS, wscale) → lo
   generó el kernel vía `connect()`.
2. `SYN-ACK` con ISN propio y `ack 3438309497` = ISN_cliente + 1.
3. `ACK` → handshake completo. El kernel informa el puerto como abierto.
4. `RST-ACK` → Nmap aborta la conexión; no le interesa hablar, solo
   confirmar que el puerto responde.

## Captura 2 — puerto cerrado

```
06:46:17.781425 IP 127.0.0.1.46849 > 127.0.0.1.22222: Flags [S], seq 2012341560, win 1024, options [mss 1460], length 0
06:46:17.781438 IP 127.0.0.1.22222 > 127.0.0.1.46849: Flags [R.], seq 0, ack 2012341561, win 0, length 0
```

SYN respondido con `RST` inmediato → puerto cerrado. (En el lab ocurrió
porque el `nc` original sin `-k` había muerto tras la conexión anterior —
recordatorio de que el estado del objetivo puede cambiar entre escaneos.)

## Captura 3 — SYN scan (`-sS`), puerto abierto (half-open)

```
20:31:46.046615 IP 127.0.0.1.44585 > 127.0.0.1.22222: Flags [S], seq 307277771, win 1024, options [mss 1460], length 0
20:31:46.046630 IP 127.0.0.1.22222 > 127.0.0.1.44585: Flags [S.], seq 3459780576, ack 307277772, win 65495, options [mss 65495], length 0
20:31:46.046636 IP 127.0.0.1.44585 > 127.0.0.1.22222: Flags [R], seq 307277772, win 0, length 0
```

Lectura:
1. `SYN` con `win 1024, mss 1460` y sin timestamps → paquete crudo de
   Nmap, firma reconocible.
2. `SYN-ACK` del servicio → puerto abierto.
3. `RST` pelado (sin ACK) con `seq 307277772` = el ack del SYN-ACK.
   **No lo envía Nmap:** lo envía el kernel local al recibir un SYN-ACK
   de una conexión que él nunca inició. Handshake incompleto = la
   aplicación que escucha no registra la conexión en sus logs.

## Comparación de firmas

| Caso | Paquetes | Señal |
|---|---|---|
| `-sT` abierto | SYN, SYN-ACK, ACK, RST | handshake completo + abort |
| cerrado | SYN, RST | RST seco |
| `-sS` abierto | SYN, SYN-ACK, RST | half-open |

## Bonus de detección

- SYN de kernel: opciones ricas (sackOK, TS, wscale, win grande).
- SYN crudo de Nmap: `win 1024, mss 1460`, sin TS.
Un IDS puede flaggear SYN scans solo por las opciones TCP.

## Autoevaluación

1. En la captura 3, ¿quién emite el RST final y por qué?
2. ¿Cómo distinguís en una captura si un SYN lo generó una aplicación
   legítima o un escáner?
3. ¿Por qué `nc -l` sin `-k` arruinó el segundo experimento?
4. Si el firewall del objetivo descartara los SYN, ¿qué verías en la
   captura del lado del atacante?
