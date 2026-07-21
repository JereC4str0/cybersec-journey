# 02 — Nmap fundamentos (lab: red doméstica)

> Sesión 002 — Bloque 02 Networking. Material de repaso.
> Referencia: Nmap Reference Guide, secciones "Host Discovery",
> "Port Scanning Basics", "Service and Version Detection".

## Host discovery — por qué importa el método

Lab real: `nmap -sn 192.168.1.0/24`

- **Sin root:** Nmap usa ICMP echo + TCP a puertos comunes (80/443).
  Resultado del lab: 3 hosts. Un teléfono Motorola NO apareció.
- **Con root (en LAN):** Nmap usa ARP. Resultado: 4 hosts — el Motorola
  apareció.

**Lección:** ARP no se puede filtrar en una red local; si un dispositivo
quiere comunicarse, debe responder ARP. Un host "caído" en un escaneo sin
root suele ser un host que filtra, no apagado. En engagements reales esto
es crítico: servidores con firewall estricto desaparecen del discovery
básico.

## Identificación de dispositivos desconocidos — orden de campo

De lo pasivo/barato a lo activo/pesado:

1. **OUI de la MAC** — los primeros 3 bytes identifican al fabricante.
   Nmap lo muestra en escaneos con root. Lab real:
   - `6C:5A:B0` → TP-Link (router)
   - `4C:BA:D7` → LG Innotek (TV)
   - `C4:A0:52` → Motorola Mobility (teléfono)
2. **`-sV`** — los servicios delatan al dispositivo (ej: puerto 3000 +
   respuesta webOS = TV LG).
3. **`-O`** — OS fingerprinting. Requiere root, al menos un puerto abierto
   y uno cerrado. Falla seguido; es complemento, no primera opción.
4. **`-sC`** — scripts por defecto: banners, mDNS, NetBIOS, etc.

## Barrido de puertos vs detección de versión — la lección de los tiempos

Lab real contra localhost:

| Comando | Puertos | Tiempo |
|---|---|---|
| `nmap -sV localhost` | 1000 (default) | 6.20 s |
| `sudo nmap -p- localhost` | 65535 | 0.37 s |

**Conclusión:** lo caro no es la cantidad de puertos, es `-sV`. Por cada
puerto abierto, Nmap abre conexiones y envía probes esperando respuestas.

Estrategia profesional:
1. `nmap -p- <host>` rápido para mapear superficie completa.
2. `nmap -sV -p <puertos_abiertos> <host>` quirúrgico.

Nmap por defecto escanea solo los 1000 puertos más comunes. Los servicios
interesantes viven seguido en puertos altos (SSH movido, paneles, Redis
6379, etc.). El default se los pierde.

## Hallazgo del lab: LLMNR (5355/tcp)

El `-p-` reveló `5355/tcp llmnr` (systemd-resolved) que el default ocultaba.

**Por qué importa:** LLMNR/NBT-NS resuelve nombres por multicast cuando
DNS falla — la máquina pregunta a gritos a toda la red. Un atacante interno
puede responder esas consultas haciéndose pasar por el destino y capturar
hashes de credenciales (herramienta: Responder). Es uno de los ataques
internos más clásicos (ver Bloque 07 — Active Directory).

Mitigación identificada (anotada para el reporte, no aplicada aún):
`LLMNR=no` en `/etc/systemd/resolved.conf`.

## Otros servicios encontrados en localhost

- `631/tcp CUPS 2.4` — impresión. Solo local → riesgo bajo, pero es
  superficie de ataque si no se usa (CUPS tuvo CVEs serios en 2024).
- `9050/tcp Tor SOCKS` — proxy local. Esperado.

Regla: cada servicio abierto es una pregunta — ¿lo uso? ¿debería estar
expuesto? ¿a qué interfaz está atado?

## Errores comunes

- Asumir que "3 hosts up" es la verdad completa sin probar discovery con ARP.
- Correr `-sV -p-` contra muchos hosts: innecesariamente lento.
- Identificar solo con `-O` cuando el OUI de la MAC ya daba la respuesta gratis.
- Publicar outputs sin sanitizar (MACs completas, IPs, hostnames).

## Autoevaluación

1. ¿Por qué ARP discovery es más confiable que ICMP en LAN?
2. ¿Cuál es el orden correcto para identificar un dispositivo desconocido?
3. ¿Qué comando usarías para mapear TODOS los puertos de 50 hosts en
   tiempo razonable, y cómo le sumás versiones después?
4. ¿Qué ataque habilita LLMNR y en qué fase de un pentest interno aparece?
