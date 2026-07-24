# TryHackMe — Enumeration & Brute Force

**Room:** https://tryhackme.com/room/enumerationbruteforce (FREE)
**Path:** Web Application Pentesting — módulo Intro
**Fecha:** 2026-07-24
**Entorno:** Arch (Omarchy) + OpenVPN propio (us-east-1, tun0 10.64.0.0/12) + Burp Suite Community + Hydra

> Nota: sin flags ni respuestas literales — solo metodología. Las credenciales
> del lab aparecen parcialmente sanitizadas.

---

## Setup de red (pre-requisito de toda room)

- VPN: `sudo openvpn --config ~/vpn/tryhackme.ovpn` → esperar `Initialization Sequence Completed`
- Verificar: `ip addr show tun0` → IP 192.168.x.x/18 + ruta 10.64.0.0/12 (ahí viven todas las VMs THM)
- `Start Machine` asigna IP efímera (~1h, extensible). **Stop/Start = IP nueva = actualizar /etc/hosts**
- vhosts: la room sirve por nombre → `echo "MACHINE_IP enum.thm" | sudo tee -a /etc/hosts`
- Update posterior: `sudo sed -i 's/.*enum\.thm.*/NUEVA_IP enum.thm/' /etc/hosts`
- Diagnóstico de conectividad: `refused` = host vivo, puerto cerrado (app booteando);
  `timeout` = firewall/host caído. Distinción clave para leer nmap después.

## Task 2 — Authentication Enumeration (concepto)

Authentication enumeration = pelar la cebolla del mecanismo de auth ANTES de atacar.
Los 4 oracles clásicos para confirmar usuarios válidos sin tocar la DB:

1. **Registro**: "este email ya está registrado" = confirmación gratis
2. **Password reset**: respuestas diferenciales según existencia del usuario
   (defensa: mensaje genérico idéntico para ambos casos)
3. **Errores verbosos de login**: "usuario no existe" vs "contraseña incorrecta" = oracle de 1 bit
4. **Brechas previas**: credential stuffing con dumps (por eso no reciclar passwords)

Vector extra: si el error revela la **regex de la política de passwords**, el atacante
genera un diccionario que CUMPLE la política → recorta el espacio de búsqueda del brute force.

## Task 3 — Enumerating Users via Verbose Errors

**Lab:** `http://enum.thm/labs/verbose_login/`

Oracle verificado a mano con curl (siempre validar manual antes de automatizar):

```
curl -s -X POST http://enum.thm/labs/verbose_login/functions.php \
  -d "username=test@test.com&password=x&function=login" \
  -H "X-Requested-With: XMLHttpRequest"
→ {"status":"error","message":"Invalid password"}   ← el email EXISTE
```

- Email inválido → "Email does not exist"; email válido + clave basura → "Invalid password"
- La contraseña es irrelevante: el oracle dispara por EXISTENCIA, no por auth
- Recon gratis en headers: `Server: Apache/2.4.41 (Ubuntu)`, `PHPSESSID`,
  `Expires: 19 Nov 1981` (firma anti-cache de sesiones PHP) → stack identificado sin escanear

**Contrato AJAX:** el header `X-Requested-With: XMLHttpRequest` activa el "modo JSON"
del backend. Form tradicional → HTML/302; AJAX → JSON. Sin el header, algunos backends
rompen el `.json()` del script. Los headers "raros" son parte del contrato, no decoración.
(Bonus: también se usa como mitigación CSRF débil — un sitio cross-origin no puede
setear headers custom sin preflight CORS. Ver room csrfV2.)

**Automatización:** script python (provisto por la room) → POST por cada email de la
lista, clasifica por `message`. Firma: `"Email does not exist" in response`.
Lista: `usernames_gmail.com.txt` (nyxgeek/username-lists, top-100).
En Arch con PEP 668: `uv run --with requests python3 script.py <lista>`.

Resultado: 1 email válido de 100 (`c***@gmail.com`) — verificable a mano con un curl.

**Uso real:** hallazgo reportable "User Enumeration via Authentication Oracle"
(severidad baja-media). En engagements: medir qué tan estricto es el contrato,
comparar respuestas, y cruzar con usernames obtenidos por OSINT (Task 6).

## Task 4 — Exploiting Vulnerable Password Reset Logic

**Lab:** `http://enum.thm/labs/predictable_tokens/`

Código vulnerable: `$token = mt_rand(100, 200);` → token de reset de 3 dígitos,
rango conocido: 101 valores. No es un token, es un PIN brute-forceable.

Fallas clásicas de reset (checklist de reporte):
tokens predecibles/secuenciales · tokens sin expiración · reutilizables ·
validación débil (security questions con PII público) · transporte sin HTTPS ·
mensajes que confirman existencia del email

Pipeline Burp Intruder (Sniper):
1. Pedir reset para el usuario objetivo → capturar `GET reset_password.php?token=###`
2. Send to Intruder → marcar el valor del token como posición
3. Diccionario: `crunch 3 3 -o otp.txt -t %%% -s 100 -e 200` (101 líneas)
4. El ganador = **Content-Length outlier** (página "set new password" vs "Invalid token")

Por qué funciona aunque el token sea "random": (a) espacio total minúsculo (101),
(b) sin rate limit ni expiración. Random ≠ seguro si el espacio es chico y no hay defensas.

Nota de herramienta: Burp Community rate-limita Intruder (~1 req/s) → 101 requests ≈ 15-20 min.

## Task 5 — Exploiting HTTP Basic Authentication

**Lab:** `http://enum.thm/labs/basic_auth/`

Basic Auth (RFC 7617): `Authorization: Basic base64(usuario:password)` en CADA request.
**base64 es encoding, NO cifrado** — reversible en 1s. Sin HTTPS = credenciales en claro.
Sigue vivo en routers/IoT/impresoras (sin capacidad de sesiones) → vector #1 en IoT.
Señal de detección: `401` + header `WWW-Authenticate: Basic` + popup nativo del browser.

Pipeline Burp Intruder (la trampa: el payload va empaquetado, no es un parámetro):
1. Posición sobre el string base64
2. Payload Processing: *Add prefix* `admin:` → *Base64-encode*
3. Payload encoding: quitar `=` del URL-encode (el `=` es padding legítimo de base64)

**Hydra — la herramienta correcta (2da pregunta de la task):**

```
hydra -l admin -P /usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt \
  enum.thm http-get /labs/basic_auth/
→ [80][http-get] host: enum.thm  login: admin  password: y*****  (~3 segundos)
```

- Hydra no necesita reglas de base64: su módulo `http-get` CONOCE el protocolo y
  empaqueta el Authorization por dentro. Burp ve el header como texto opaco.
- Comparación medida: Hydra ~3s vs Burp Community ~2min (misma wordlist) —
  16 conexiones paralelas + sin rate limit.
- Regla: tools protocol-aware (hydra/medusa/ncrack) para auth conocida;
  Burp Intruder para esquemas custom.
- `pacman -Ql <paquete>` lista todo lo que instaló un paquete (para encontrar wordlists).

## Task 6 — OSINT (Wayback URLs + Google Dorks)

Recon PASIVO: no toca el objetivo, no deja logs. Va ANTES de la enumeration activa.

```
go install github.com/tomnomnom/waybackurls@latest   # queda en ~/go/bin (agregar al PATH)
waybackurls <dominio>                                  # dump de URLs archivadas
```

Lectura del output crudo: incluye ruido archivado — fuzzing histórico de terceros
(`%22`, `%0A` = CRLF injection attempts de otros), reviews de usuarios capturadas
como URLs relativas. El trabajo es FILTRAR:

```
waybackurls <dom> | grep -Ei '\.(sql|bak|zip|env|config|log|old)(\?|$)'   # reliquias
waybackurls <dom> | grep -v '%' | cut -d/ -f4 | sort -u                    # mapa de rutas
waybackurls <dom> | grep '?' | grep -v '%'                                 # superficie con parámetros
```

Hallazgos reales en el ejemplo: usernames históricos (esquema viejo de perfiles →
user enumeration pasiva → alimenta wordlists de Task 3) y bundles JS hasheados
(JS recon: endpoints deprecados, keys hardcodeadas en builds viejos).

Google Dorks (catálogo: exploit-db.com/google-hacking-database):

```
site:<dom> inurl:admin          paneles
site:<dom> filetype:log         logs
site:<dom> intitle:"index of"   dir listing abierto
site:<dom> ext:sql | ext:bak    backups
```

Límite legal: mirar (pasivo) ≠ usar. Encontrar un panel con un dork = recon; tocarlo = intrusión.

## Secuencia mental para engagements (síntesis de la room)

```
OSINT pasivo (wayback/dorks, sin logs)
  → enumeration activa (oracles de login/reset/registro)
  → brute force dirigido (wordlist que cumple la política, hydra/burp)
  → post-acceso
```

---

## Auto-evaluación (responder sin mirar)

1. ¿Qué diferencia hay entre `Connection refused` y `timeout` al probar un puerto?
2. ¿Por qué en el oracle de verbose login la contraseña puede ser cualquiera?
3. ¿Qué hace `X-Requested-With` y por qué un script puede romperse sin él?
4. `mt_rand(100,200)` es random — ¿por qué es brute-forceable igual? (2 razones)
5. ¿Por qué Hydra no necesita las payload rules de base64 que Burp sí?
6. Ordená: brute force / OSINT pasivo / enumeration de oracles. ¿Por qué ese orden?

## Errores propios encontrados (bitácora)

- `pkill -f <patrón>` puede matar tu propio shell (el patrón matchea tu comando) → usar `pkill -x`
- IP efímera de THM: tras Stop/Start, `/etc/hosts` queda stale → sed para actualizar
- Burp `UnsupportedClassVersionError`: class file 65 = Java 21, 61 = Java 17;
  la JVM corre hacia atrás, no hacia adelante → `archlinux-java set`
- Wayland/XWayland: fuentes feas en apps Swing → flags `-Dawt.useSystemAAFontSettings=on -Dswing.aatext=true`
