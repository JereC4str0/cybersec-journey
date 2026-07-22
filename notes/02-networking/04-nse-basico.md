# NSE (Nmap Scripting Engine) — repaso

> Sesión 003, Parte A. Lab: localhost, servicios propios. Entorno autorizado.

## Comandos

```bash
# NSE por defecto contra un servicio vivo
nmap -sV -sC -p 8000 localhost

# Script específico
nmap --script ssh2-enum-algos -p 22 localhost
```

## Concepto

NSE es el motor de scripts de Nmap (escritos en Lua). Extiende el escaneo
de "qué puerto está abierto" a "qué puedo averiguar DEL servicio".

- `-sC` = ejecuta los scripts de la categoría `default`: scripts seguros,
  no intrusivos, orientados a descubrimiento. Es el estándar en enum inicial.
- `--script <nombre>` = ejecuta un script puntual (o varios separados por
  coma, o una categoría entera como `vuln`, `auth`, `discovery`).
- Los scripts se agrupan en categorías: `default`, `discovery`, `safe`,
  `intrusive`, `vuln`, `auth`, `brute`, `malware`, `dos`, `exploit`.

**Regla de oro (aprendida en lab): los scripts NSE solo se ejecutan contra
puertos ABIERTOS y servicios que reconocen.** Con el puerto 22 cerrado,
`-sC` no disparó nada y `ssh2-enum-algos` no tuvo a quién interrogar.

## Evidencia del lab (2026-07-21)

Servicio levantado para la prueba:

```bash
python3 -m http.server 8000 &
```

Output del escaneo:

```
PORT     STATE SERVICE VERSION
8000/tcp open  http    SimpleHTTPServer 0.6 (Python 3.14.6)
|_http-server-header: SimpleHTTP/0.6 Python/3.14.6
|_http-title: Directory listing for /
```

Dos scripts `default` dispararon:

1. `http-server-header` → expone software y versión exacta
   (`SimpleHTTP/0.6 Python/3.14.6`).
2. `http-title` → revela que el servicio sirve un listado de directorios.

Bonus observado: el log del servidor Python registró las peticiones de
Nmap (`OPTIONS / HTTP/1.1`, `GET / HTTP/1.0`, `GET / HTTP/1.1`) —
evidencia de que NSE genera tráfico detectable del lado del objetivo.

### Segunda evidencia: `ssh2-enum-algos` contra OpenSSH propio

```
PORT   STATE SERVICE
22/tcp open  ssh
| ssh2-enum-algos:
|   kex_algorithms: (10)
|       mlkem768x25519-sha256
|       sntrup761x25519-sha512
|       curve25519-sha256
|       ecdh-sha2-nistp256 ...
|   server_host_key_algorithms: (4)
|       rsa-sha2-512, rsa-sha2-256, ecdsa-sha2-nistp256, ssh-ed25519
|   encryption_algorithms: (6)
|       chacha20-poly1305@openssh.com, aes128-gcm@openssh.com,
|       aes256-gcm@openssh.com, aes128-ctr, aes192-ctr, aes256-ctr
|   mac_algorithms: (10)
|       ...-etm@openssh.com (preferidos), hmac-sha2-*, hmac-sha1
|   compression_algorithms: (2)
|_      none, zlib@openssh.com
```

**Análisis de auditoría: configuración FUERTE. Sin hallazgos.**

- **KEX**: ofrece `mlkem768x25519-sha256` y `sntrup761x25519-sha512` —
  intercambio de claves **post-cuántico** (híbrido). OpenSSH moderno.
  `curve25519` y `ecdh-sha2` también presentes. Todo aceptable.
- **Host key**: `rsa-sha2-*` (SHA-2), `ecdsa`, `ed25519`. NO ofrece el
  deprecado `ssh-rsa` (SHA-1). Correcto.
- **Cifrado**: solo AEAD (`chacha20-poly1305`, `aes-gcm`) y `aes-ctr`.
  NO hay CBC. Correcto.
- **MAC**: variantes `-etm` (encrypt-then-mac) listadas primero — el
  orden importa: el server las prefiere. `hmac-sha1` está disponible
  como fallback → observación menor, no hallazgo (solo se usa si el
  cliente lo negocia).
- **Compresión**: `none` primero. Correcto (la compresión en SSH puede
  facilitar fugas de información tipo CRIME).

**Lección clave:** un output de enum también se reporta cuando NO hay
problemas. En un informe real esto sería "SSH hardening verificado —
algoritmos modernos, sin deprecated". Un auditor que solo reporta
problemas y no verifica fortalezas da una imagen incompleta del riesgo.

**Cómo se vería una config DÉBIL (para comparar):** `diffie-hellman-group1-sha1`
(768-bit, roto), `ssh-rsa` solo, cifrados `*-cbc`, `3des-cbc`, MACs
`-md5`. Contra una VM vieja (como Kioptrix) esperá ver exactamente eso.

## Por qué le importa a un pentester

- **Version disclosure** (`http-server-header`): conocer software+versión
  exacta permite buscar CVEs públicos. En una auditoría, un banner que
  revela versión es un hallazgo reportable de severidad baja/informativa.
- **Directory listing** (`http-title`): un listado de directorios expuesto
  puede filtrar archivos internos, backups, credenciales. Hallazgo clásico.
- **ssh2-enum-algos**: lista los algoritmos de cifrado/intercambio de
  claves que ofrece un SSH. Algoritmos débiles o deprecados (SHA-1,
  CBC, `ssh-rsa` viejo) son reportables en auditorías reales.
- **Detectabilidad**: NSE hace requests reales al servicio. Queda en logs.
  En un engagement con scope sigiloso, `-sC` ya puede ser demasiado ruido;
  se decide conscientemente, no por defecto.

## Errores comunes

- Correr NSE contra un puerto cerrado y creer que "no hay nada" —
  simplemente nunca se ejecutó.
- Usar `--script vuln` a ciegas: puede ser intrusivo y lento. Primero
  saber qué servicios hay, después elegir scripts puntuales.
- Ignorar que el tráfico NSE queda logueado del otro lado.

## Variantes útiles

```bash
nmap --script default,safe -p 80 target      # varias categorías
nmap --script http-enum -p 80 target          # enum de paths web comunes
nmap --script vuln -p 443 target              # chequeos de vulns conocidas
nmap --script-args http.useragent="Mozilla"   # pasar argumentos a scripts
ls /usr/share/nmap/scripts/                   # todos los scripts instalados
nmap --script-help http-title                 # documentación de un script
```

## Autoevaluación

1. ¿Qué categoría de scripts corre `-sC` y qué la caracteriza?
2. ¿Por qué `ssh2-enum-algos` no devolvió nada con el puerto 22 cerrado?
3. Dado el hallazgo `http-server-header: SimpleHTTP/0.6 Python/3.14.6`,
   ¿cuál es el siguiente paso de investigación?
4. ¿Por qué `-sC` puede ser indeseable en un engagement sigiloso?
5. ¿Qué diferencia hay entre `--script http-title` y `--script vuln`
   en términos de riesgo para el objetivo?
