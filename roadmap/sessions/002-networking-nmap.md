# Sesión 002 — Bloque 02: Networking para pentesting

> Modo profesor: cada ejercicio viene con su material de estudio exacto.
> No avanzar a web/AD sin cerrar la exit gate de este bloque.

## Por qué este bloque ahora

Bandit 0-32 cubrió Linux/Git (Bloque 01, prácticamente cerrado).
Networking es la base de todo lo que sigue: web, AD, cloud. Sin esto,
las máquinas se resuelven copiando comandos sin entenderlos.

## Objetivo del bloque

Poder enumerar un host/red, explicar qué encontró Nmap, por qué importa
cada puerto abierto, y leer una captura de tráfico básica.

## Material de estudio (gratuito, exacto)

1. **Nmap Reference Guide** (oficial, gratis): https://nmap.org/book/man.html
   - Sección "Port Scanning Basics" — los 6 estados de puerto.
   - Sección "Host Discovery" — `-sn`, `-Pn`, por qué importa.
2. **The TCP/IP Guide** (gratis online): http://www.tcpipguide.com/free/
   - TCP: three-way handshake (SYN, SYN-ACK, ACK) — solo esa sección.
   - UDP vs TCP: diferencias y por qué el escaneo UDP es lento.
3. **Wireshark docs**: https://wiki.wireshark.com/FrontPage
   - Solo: capturar en una interfaz y aplicar display filters (`tcp`, `dns`, `http`).

## Teoría mínima (alcance cerrado)

- Modelo OSI vs TCP/IP: solo capas 2-4 y dónde vive cada protocolo.
- TCP vs UDP; handshake de 3 vías; estados de puerto (open, closed, filtered).
- DNS y HTTP como protocolos de aplicación que vas a ver en capturas.
- Qué hace Nmap por defecto y qué cambia con `-sS`, `-sV`, `-O`, `-sC`, `-p-`.

"Entendido" significa: podés explicar con tus palabras qué pasa cuando
Nmap marca un puerto como `filtered` y por qué un SYN scan es sigiloso
relativo a un connect scan.

## Práctica (entregables)

Todo contra localhost, tu propia red /24 o VMs propias. Nada externo.

1. **Host discovery**: descubrir hosts vivos en tu red local.
   - Identificar tu subred (`ip a`), escanear con ping scan.
   - Anotar: ¿qué dispositivos aparecen? ¿reconocés todos?
2. **Service detection**: escanear tu propia máquina completo.
   - Todos los puertos, detección de servicio y versión.
   - Anotar cada servicio encontrado y si debería estar expuesto.
3. **NSE básico**: correr scripts por defecto contra un servicio propio
   (por ejemplo SSH local) y explicar 2 hallazgos del output.
4. **Captura**: capturar con Wireshark/tcpdump un escaneo propio y
   encontrar el handshake SYN/SYN-ACK/ACK en la captura.

## Desafío extra

- Comparar tiempo y resultados de connect scan vs SYN scan vs `-sV`.
- Documentar cuál genera más ruido en logs y por qué.

## Entregables públicos

- `notes/02-networking/01-osi-tcpip.md`
- `notes/02-networking/02-nmap-fundamentos.md`
- `notes/02-networking/03-captura-handshake.md` (con captura sanitizada)
- `cheatsheets/nmap.md` mejorado (ya existe: expandir con lo aprendido)
- Todo output sanitizado: sin IPs públicas, sin MACs completas, sin hostnames identificables.

## Exit gate

- [ ] Explicar el output de un escaneo sin consultar documentación.
- [ ] 3 ejemplos documentados: host discovery, service detection, NSE.
- [ ] 1 captura con el handshake identificado y explicado.

## Criterio de cierre de sesión

La sesión se cierra cuando los 3 notes + cheatsheet están commiteados
y la exit gate se puede marcar honestamente.
