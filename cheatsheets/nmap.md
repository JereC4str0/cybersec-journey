# Nmap Cheatsheet

> Referencia rápida. Detalle y lecciones: `notes/02-networking/`.
> Uso ético: solo contra hosts propios o con autorización escrita.

## Host discovery
```bash
nmap -sn 192.168.1.0/24          # ping scan (sin root: ICMP+TCP 80/443)
sudo nmap -sn 192.168.1.0/24     # en LAN usa ARP: más confiable, muestra MACs/OUI
nmap -Pn target                  # salta discovery (asume host vivo; para hosts que filtran ping)
```

## Barrido de puertos
```bash
nmap target                      # 1000 puertos más comunes
nmap -p- target                  # los 65535 (rápido sin -sV)
nmap -p 22,80,443 target         # lista específica
nmap -p 1-1024 target            # rango
nmap --top-ports 100 target      # top N por frecuencia
```

## Tipos de scan
```bash
nmap -sT target                  # connect scan: handshake completo, no requiere root, más ruidoso
sudo nmap -sS target             # SYN scan "half-open": default con root, no completa la conexión
sudo nmap -sU target             # UDP scan (lento; DNS 53, SNMP 161, etc.)
```

## Detección
```bash
nmap -sV target                  # versión de servicios (LO CARO: usar solo sobre puertos abiertos)
nmap -sC target                  # scripts por defecto (banners, mDNS, etc.)
sudo nmap -O target              # OS fingerprinting (necesita puerto abierto+cerrado; a veces falla)
nmap -A target                   # -sV + -sC + -O + traceroute
```

## Estrategia profesional (rápida y completa)
```bash
nmap -p- -oA superficie target                 # 1) superficie completa, sin -sV
nmap -sV -sC -p 22,80,6379 -oA detalle target  # 2) versiones solo sobre lo abierto
```

## Identificación de dispositivos (orden de campo)
1. OUI de la MAC (gratis, aparece con root en LAN)
2. `-sV` — servicios delatan al dispositivo
3. `-O` — complemento con sudo
4. `-sC` — banners, mDNS, NetBIOS

## Output
```bash
nmap -oA output target           # .nmap + .gnmap + .xml
nmap -oN salida.txt target       # formato normal
```

## Firmas en captura (ver notes/02-networking/03)
```
-sT abierto:  SYN, SYN-ACK, ACK, RST
cerrado:      SYN, RST
-sS abierto:  SYN, SYN-ACK, RST   (half-open; firma Nmap: win 1024, mss 1460)
```

## Sanitización antes de publicar
- MACs: `XX:XX:XX:DC:4F:98`
- IPs públicas/identificables: truncar octetos
- Hostnames internos: genéricos (`router`, `host-01`)
