# Kioptrix Level 1 — Enumeración

> Lab local propio: VM Kioptrix L1 (VulnHub) en VirtualBox, red host-only
> (192.168.56.0/24). Objetivo: 192.168.56.102. Entorno 100% autorizado.
>
> Sesión 003, Parte B — primera máquina vulnerable del portfolio.

## Comandos

```bash
# Fase 1: barrido completo de puertos (rápido, SYN)
sudo nmap -p- --open -sS --min-rate 2000 -v -n 192.168.56.102

# Fase 2: detección de servicio/versión + NSE default sobre los abiertos
nmap -sCV -p 22,80,111,139,443,32768 192.168.56.102 -oN enum.txt
```

## Identificación del objetivo (incidente y lección)

Primer intento de enum salió contra 192.168.56.101, que mostraba
OpenSSH 10.4 — imposible para una VM del 2009. Diagnóstico:

- El host (mi máquina) tenía una **IP secundaria por DHCP** en vboxnet0
  (NetworkManager/systemd pidió lease al DHCP de VirtualBox).
- El escaneo golpeaba mi propio sshd y un `nc` colgado en 22222.
- La pista delataba al falso positivo: mDNS resolvía `.101` como
  `1312.local` (mi hostname).

**Lecciones de recon:**

1. Verificar QUÉ es un host antes de analizarlo: MAC vendor
   (`08:00:27` = VirtualBox), hostname mDNS, versiones esperadas.
2. Conocer la propia infraestructura del lab: qué IPs tiene el host,
   qué servicios propios están escuchando.
3. Una versión "demasiado moderna" para el contexto es una red flag
   igual de válida que una demasiado vieja.
4. Limpieza post-lab: `ip addr del` de IPs DHCP fantasma, matar
   listeners de práctica (`nc`), apagar servicios levantados para el lab.

## Resultado de la enumeración

| Puerto | Servicio | Versión | Notas NSE |
|--------|----------|---------|-----------|
| 22/tcp | SSH | OpenSSH 2.9p2 (protocol 1.99) | Soporta SSHv1; hostkeys RSA1/DSA/RSA de 1024 bits |
| 80/tcp | HTTP | Apache 1.3.20 (Red-Hat) mod_ssl/2.8.4 OpenSSL/0.9.6b | Title: test page Red Hat; método TRACE habilitado |
| 111/tcp | rpcbind | 2 (RPC #100000) | rpcinfo: también `status` (#100024) en 32768 |
| 139/tcp | netbios-ssn | Samba smbd (workgroup: MYGROUP) | NetBIOS name: KIOPTRIX; SMB2 negotiation failed → solo SMB1 |
| 443/tcp | HTTPS | Apache 1.3.20 mod_ssl/2.8.4 OpenSSL/0.9.6b | SSLv2 soportado con cifrados EXPORT; cert vencido 2010, autofirmado |
| 32768/tcp | status | 1 (RPC #100024) | Servicio RPC `status` (rpc.statd) |

Extras: `clock-skew` ~4h (reloj de la VM desfasado); 445/tcp closed.

## Análisis por servicio (pensando como atacante)

### 22 — OpenSSH 2.9p2

- **SSHv1 habilitado**: protocolo con debilidades de diseño conocidas
  (sin integridad fuerte, vulnerable a inserción). Hallazgo reportable.
- Claves de 1024 bits: por debajo del mínimo actual (2048+).
- OpenSSH 2.9p2 es de 2001: existen exploits históricos, pero en la
  práctica SSH rara vez es la vía más directa en esta máquina.

### 80/443 — Apache 1.3.20 + mod_ssl 2.8.4 + OpenSSL 0.9.6b

- **Mismo servicio en dos puertos** (HTTP y HTTPS): el contenido es el
  mismo; 443 agrega la capa TLS. Enumerar ambos es obligatorio.
- `mod_ssl 2.8.4` con `OpenSSL 0.9.6b`: corresponde a la era del
  famoso desbordamiento de buffer en mod_ssl (CVE-2002-0082,
  familia de exploits "OpenFuck"). Vector clásico de esta máquina.
- **SSLv2 con cifrados EXPORT (40 bits)**: criptografía rota por
  diseño (limitaciones de exportación de los 90). Relacionado con
  DROWN. Hallazgo crítico en cualquier auditoría moderna.
- Certificado autofirmado, vencido en 2010, CN=localhost.localdomain.
- `TRACE` habilitado: permite Cross-Site Tracing (robo de cookies
  HttpOnly en escenarios con XSS). Hallazgo menor hoy, clásico en reportes.

### 139 — Samba (SMB1 únicamente)

- `smb2-time: Protocol negotiation failed` → el server solo habla
  **SMB1**, protocolo obsoleto y peligroso (era WannaCry/EternalBlue,
  aunque eso es Windows; en Linux el riesgo es Samba viejo).
- Kioptrix L1 corre Samba 2.2.1a: vulnerable a **trans2open**
  (CVE-2003-0201), RCE remoto como root. El otro vector clásico.
- Workgroup MYGROUP + NetBIOS KIOPTRIX: fingerprinting completo.

### 111/32768 — rpcbind + rpc.statd

- rpcbind expone el mapa de servicios RPC: información gratuita para
  el atacante (qué servicios RPC corren y en qué puerto).
- `rpc.statd` (#100024) viejo tiene historial de RCE (format string,
  CVE-2000-0666). Tercer candidato, menos directo que los otros dos.

## Ranking de superficie de ataque (hipótesis pre-explotación)

1. **Samba 2.2.1a (139)** — trans2open: RCE remoto directo como root.
2. **mod_ssl/OpenSSL (443)** — "OpenFuck": RCE remoto (apache → root
   vía variante). Requiere compilación del exploit viejo.
3. rpc.statd (32768) — posible, más frágil.
4. OpenSSH 2.9p2 (22) — débil en configuración, no la vía práctica.

Hipótesis a validar en sesión 004 (explotación guiada).

## Detección / mirada blue team

- El SYN scan a 65535 puertos generó ~66k paquetes: ruido brutal,
  detectable por cualquier IDS. En engagement real: escaneos por
  etapas, `--top-ports`, horarios acordados.
- Los scripts NSE (`sslv2`, `nbstat`, `sshv1`) hacen handshakes reales:
  quedan en logs de Apache/SSH/Samba.
- Defensa contra lo encontrado: deshabilitar SSHv1, SSLv2 y SMB1;
  actualizar Apache/Samba/OpenSSH; no exponer rpcbind; certificados
  válidos; deshabilitar TRACE (`TraceEnable Off`).

## Autoevaluación

1. ¿Por qué el primer escaneo contra .101 mostró OpenSSH 10.4 y qué
   tres señales lo delataban?
2. ¿Qué diferencia hay entre los hallazgos del puerto 80 y el 443 si
   "es el mismo Apache"?
3. ¿Por qué SSLv2 con cifrados EXPORT es crítico y no "viejo pero
   menor"?
4. ¿Qué información regaló rpcbind sin autenticación?
5. ¿Qué significa que SMB2 negotiation falle en un server 2026? ¿Y por
   qué en esta VM es esperable?
6. Rankeá los 4 vectores candidatos y justificá el orden.
