# Semana 1: Fundamentos, Linux y Networking

> **Objetivo semanal:** Reforzar redes, Linux y scripting básico para que el resto del camino sea más fácil. Terminarás con tu primer script propio: un port scanner en Python.
>
> **Carga diaria:** 4-5 horas totales.
> **Distribución recomendada:** 1.5h teoría + 2.5h práctica + 1h documentación/revisión.
> **Entregable final de semana:** Port scanner v1.0 en `scripts/port-scanner/`, writeup de Bandit en `labs/overthewire/`, notas de networking en `notes/02-networking/`.

---

## Día 1 — Modelo OSI/TCP-IP + Linux básico

### Teoría (1.5h)
- [ ] Leer sobre el modelo OSI y TCP/IP.
- [ ] Entender las diferencias entre TCP, UDP, IP, ICMP.
- [ ] Conceptos básicos de puertos, sockets, handshake de 3 vías.

**Recursos:**
- Cisco Skills for All — Networking Essentials (gratis, en español/inglés).
- [Cloudflare: What is the OSI model?](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
- [RFC 793: TCP](https://tools.ietf.org/html/rfc793) (resumen básico nada más).

### Práctica (2.5h)
- [ ] Completar OverTheWire Bandit niveles 0-10.
- [ ] Familiarizarte con: `ssh`, `ls`, `cat`, `find`, `grep`, `file`, `strings`, `base64`, `tr`.

### Documentación (1h)
- [ ] Crear notas en `notes/02-networking/01-osi-tcpip.md`.
- [ ] Crear `labs/overthewire/bandit-writeup.md` y empezar a registrar los niveles resueltos.

### Desafío del día
> Encontrar la contraseña del nivel 10 sin mirar soluciones online. Anotar cada comando usado.

---

## Día 2 — DNS, HTTP, Nmap y Bandit avanzado

### Teoría (1.5h)
- [ ] DNS: resolución, registros (A, AAAA, CNAME, MX, TXT, NS), cacheo.
- [ ] HTTP/HTTPS: métodos, status codes, headers, request/response básico.

**Recursos:**
- [Mozilla MDN: HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [How DNS Works](https://howdns.works/)

### Práctica (2.5h)
- [ ] Completar OverTheWire Bandit niveles 11-20.
- [ ] Usar `nslookup`, `dig`, `host` para resolver dominios.
- [ ] Primeros pasos con Nmap: `nmap -sT`, `nmap -sV`, `nmap -sC`.

### Documentación (1h)
- [ ] Agregar `notes/02-networking/02-dns-http.md`.
- [ ] Actualizar writeup de Bandit.

### Desafío del día
> Escanear tu propia máquina local con Nmap y listar los 10 puertos más comunes. ¿Qué servicios están corriendo?

---

## Día 3 — Nmap en profundidad + escaneo de redes

### Teoría (1.5h)
- [ ] Tipos de escaneo Nmap: SYN, Connect, UDP, ACK, Window, FIN/NULL/Xmas.
- [ ] Timing templates (`-T0` a `--T5`) y evasión básica.
- [ ] Output formats: normal, XML, grepable, all (`-oA`).

**Recursos:**
- [Nmap Network Scanning (libro oficial, capítulos 1-5)](https://nmap.org/book/)
- `man nmap`

### Práctica (2.5h)
- [ ] Escanear una máquina VulnHub local o tu router local (con autorización).
- [ ] Experimentar con: `-p-`, `-sV`, `-sC`, `-O`, `-A`, `--script vuln`.
- [ ] Completar Bandit 21-27 si no lo hiciste.

### Documentación (1h)
- [ ] Actualizar `cheatsheets/nmap.md` con comandos aprendidos.
- [ ] Subir capturas de salidas de Nmap (sin IPs sensibles) a `notes/02-networking/03-nmap-practice.md`.

### Desafío del día
> Realizar un escaneo completo de todos los puertos a una máquina vulnerable local y exportar el resultado a los 3 formatos de Nmap.

---

## Día 4 — Python para redes: sockets y threading

### Teoría (1.5h)
- [ ] Módulo `socket` de Python.
- [ ] Módulo `threading` y `concurrent.futures` para concurrencia.
- [ ] Manejo de argumentos con `argparse`.

**Recursos:**
- [Python socket documentation](https://docs.python.org/3/library/socket.html)
- [Real Python: Threading in Python](https://realpython.com/intro-to-python-threading/)

### Práctica (2.5h)
- [ ] Escribir un script que intente conectar a un solo puerto TCP de un host.
- [ ] Extenderlo para escanear un rango de puertos con threads.
- [ ] Agregar `argparse` para recibir IP, rango de puertos y número de threads.

### Documentación (1h)
- [ ] Crear `scripts/port-scanner/README.md` con descripción y uso.
- [ ] Crear `scripts/port-scanner/portscanner.py`.

### Desafío del día
> Tu script debe poder ejecutarse así: `python3 portscanner.py -t 127.0.0.1 -p 1-65535 -T 100` y mostrar puertos abiertos.

---

## Día 5 — Mejorar el port scanner

### Teoría (1.5h)
- [ ] Cómo detectar banners de servicios.
- [ ] Manejo de timeouts y errores en sockets.
- [ ] Estructura básica de un proyecto Python (main, funciones, tests).

### Práctica (2.5h)
- [ ] Agregar banner grabbing básico (HTTP, SSH, FTP).
- [ ] Agregar output a JSON/CSV.
- [ ] Manejar excepciones (host inalcanzable, timeout).
- [ ] Probar el script contra tu máquina local y una VulnHub.

### Documentación (1h)
- [ ] Actualizar README del script con ejemplos de uso.
- [ ] Agregar `scripts/port-scanner/.gitignore` para archivos de output.

### Desafío del día
> El script debe identificar al menos 3 servicios distintos por banner y exportar los resultados a un CSV.

---

## Día 6 — Integración, testing y documentación

### Teoría (1.5h)
- [ ] Introducción a tests unitarios con `pytest`.
- [ ] Por qué testear código de seguridad (y cómo no romper tu entorno).

### Práctica (2.5h)
- [ ] Escribir 2-3 tests básicos para el port scanner (puerto válido, rango inválido, parseo de args).
- [ ] Limpiar el código: refactorizar funciones largas, agregar docstrings.
- [ ] Probar el script contra máquina VulnHub o HTB (máquina gratuita) con autorización.

### Documentación (1h)
- [ ] Actualizar `scripts/port-scanner/README.md` con arquitectura del script.
- [ ] Crear `scripts/port-scanner/tests/test_portscanner.py`.

### Desafío del día
> El script debe pasar tus tests y funcionar contra una máquina real sin errores.

---

## Día 7 — Revisión, semana de cierre y push

### Teoría (1h)
- [ ] Revisar notas de la semana.
- [ ] Leer 3 writeups de máquinas fáciles para entender formato y estilo.

**Recursos:**
- [0xdf hacks stuff](https://0xdf.gitlab.io/)
- [Ippsec](https://www.youtube.com/c/ippsec) (ver un video de máquina easy)

### Práctica (2h)
- [ ] Resolver los últimos niveles de Bandit si quedaron pendientes.
- [ ] Hacer un último test del port scanner.
- [ ] Commit y push de todo al repo.

### Documentación (1-2h)
- [ ] Actualizar README principal si es necesario.
- [ ] Actualizar `labs/tracking.md` con lo logrado esta semana.
- [ ] Escribir un breve resumen de la semana en `notes/00-fundamentos/semana-01-resumen.md`.

### Desafío final de la semana
> Publicar tu port scanner en el repo y lograr que alguien (o tú mismo en otra máquina) pueda clonar el repo y ejecutarlo sin errores con las instrucciones del README.

---

## Checklist de entregables de la semana

- [ ] OverTheWire Bandit completado (niveles 0-27 aprox).
- [ ] Notas de networking: OSI, TCP/IP, DNS, HTTP, Nmap.
- [ ] `cheatsheets/nmap.md` actualizado.
- [ ] `scripts/port-scanner/portscanner.py` funcional.
- [ ] `scripts/port-scanner/README.md` con uso y ejemplos.
- [ ] Tests básicos en `scripts/port-scanner/tests/`.
- [ ] `labs/overthewire/bandit-writeup.md` con tus soluciones y aprendizajes.
- [ ] `labs/tracking.md` actualizado.
- [ ] Todo commiteado y pusheado a GitHub.

---

## Recordatorios

- **Todas las prácticas de escaneo deben ser contra máquinas que controles o que sean de entrenamiento autorizado.**
- **No escanees redes públicas, routers de terceros ni dispositivos ajenos.**
- **Documentá todo: la documentación es parte del trabajo de un pentester.**
