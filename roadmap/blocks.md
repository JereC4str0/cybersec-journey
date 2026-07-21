# Bloques de dominio — Red Team Portfolio Edition

> Referencia técnica externa: https://roadmap.sh/cyber-security
>
> Criterio: completitud para empleabilidad, no completitud enciclopédica.

## Índice

- Bloque 00 — Sistema de evidencia pública
- Bloque 01 — Linux y Git para trabajo de seguridad
- Bloque 02 — Networking para pentesting
- Bloque 03 — Python desde 0 para security tooling
- Bloque 04 — Web security y API testing
- Bloque 05 — Metodología, vulnerability assessment y reportes
- Bloque 06 — Privilege escalation Linux/Windows
- Bloque 07 — Active Directory e internal pentesting
- Bloque 08 — Post-explotación, pivoting y C2 en lab
- Bloque 09 — Cloud security fundamentals
- Bloque 10 — Go desde 0 para herramientas
- Bloque 11 — Detección y defensa para pensar como blue team
- Bloque 12 — Portfolio final, entrevistas y búsqueda laboral

---

## Bloque 00 — Sistema de evidencia pública

**English summary:** Set up the public evidence system that will prove progress to employers.

**Objetivo:** Dejar el repo listo para documentar progreso con calidad profesional.

**Por qué importa para conseguir trabajo:** un empleador debe entender en 2 minutos qué sabés, qué hiciste y dónde verlo.

**Alcance:**
- Estructura del repo.
- Convención de commits.
- Templates de writeup/reporte.
- Sanitización de evidencias.

**Entregables públicos:**
- `roadmap/` creado.
- `templates/writeup-template.md`.
- `templates/report-template.md`.
- README principal con roadmap visible.

**Exit gate:**
- [ ] Cualquier persona puede clonar el repo y entender la ruta actual.
- [ ] Hay al menos un ejemplo de writeup con formato profesional.

**Referencia roadmap.sh:** base transversal; no aparece como nodo único, pero sostiene todo el roadmap.

---

## Bloque 01 — Linux y Git para trabajo de seguridad

**English summary:** Prove Linux and Git competence through security-oriented notes and labs.

**Objetivo:** Convertir tu base de Linux en evidencia útil para seguridad.

**Por qué importa:** Linux y Git son requisito silencioso en casi todo rol técnico de seguridad.

**Alcance:**
- Archivos, permisos, procesos, servicios, logs, usuarios.
- SSH, claves, túneles básicos.
- Git para auditoría: historial, ramas, tags, hooks, secretos.
- Bash útil para automatización.

**Entregables públicos:**
- `notes/01-linux/`
- `notes/04-git-security/`
- `labs/overthewire/bandit/` ya completo, enlazado como evidencia.
- `cheatsheets/linux.md`
- `cheatsheets/git-security.md`

**Exit gate:**
- [ ] Bandit está enlazado desde el roadmap y resume lecciones ofensivas/defensivas.
- [ ] Hay una nota de Git security con hallazgos tipo secrets en historial/ramas/tags.

**Referencia roadmap.sh:** Fundamental IT Skills, Linux, Programming/Scripting.

---

## Bloque 02 — Networking para pentesting

**English summary:** Networking knowledge translated into scanning, enumeration, and analysis deliverables.

**Objetivo:** Entender redes lo suficiente para enumerar, priorizar y explicar riesgos.

**Por qué importa:** sin networking sólido, web/AD/cloud quedan frágiles.

**Alcance:**
- OSI/TCP-IP aplicado.
- TCP/UDP/ICMP/DNS/HTTP/TLS.
- Subnetting básico.
- Nmap real: descubrimiento, servicios, scripts, output.
- Captura y lectura básica de tráfico con Wireshark/tcpdump.

**Entregables públicos:**
- `notes/02-networking/`
- `cheatsheets/nmap.md`
- `cheatsheets/wireshark.md`
- Evidencia de escaneos en lab sanitizada.

**Exit gate:**
- [ ] Podés explicar qué encontró Nmap y por qué importa.
- [ ] Tenés al menos 3 ejemplos documentados: host discovery, service detection, NSE útil.

**Referencia roadmap.sh:** Basics of Computer Networking, Security fundamentals.

---

## Bloque 03 — Python desde 0 para security tooling

**English summary:** Learn Python from zero by building security tools, not generic exercises.

**Objetivo:** Aprender Python desde 0 con salida profesional: CLI, tests, README, empaquetado.

**Por qué importa:** scripting propio es una de las pruebas más fuertes de capacidad técnica.

**Alcance:**
- Sintaxis base, errores, archivos, módulos.
- `argparse`, type hints, `uv`, `pytest`, `ruff`.
- Sockets, HTTP, concurrencia I/O-bound.
- JSON/CSV, logging, diseño CLI.

**Entregables públicos:**
- `scripts/port-scanner/`
- `scripts/enumerators/http-enum.py`
- Tests y README reproducibles.
- Benchmarks de concurrencia.

**Exit gate:**
- [ ] `uv run pytest` pasa desde clone limpio.
- [ ] Las herramientas tienen README con instalación, uso, ejemplos y limitaciones éticas.

**Referencia roadmap.sh:** Programming Skills / Python.

---

## Bloque 04 — Web security y API testing

**English summary:** Practical web and API security with PortSwigger-style evidence and original notes.

**Objetivo:** Dominar vulnerabilidades web comunes y explicar impacto real.

**Por qué importa:** web/API sigue siendo la puerta de entrada más común a roles junior de pentesting.

**Alcance:**
- HTTP moderno, cookies, sesiones, CORS, JWT.
- OWASP Top 10.
- SQLi, XSS, IDOR, access control, auth, SSRF, XXE, upload, command injection.
- API recon, métodos, mass assignment, rate limiting.
- Burp Suite Community / ZAP.

**Entregables públicos:**
- `notes/06-web-security/`
- `labs/portswigger/`
- `labs/api-testing/`
- `scripts/web-fuzzer/` o dirbuster propio.
- Writeups con impacto, detección y mitigación.

**Exit gate:**
- [ ] 30+ labs documentados con formato consistente.
- [ ] Al menos 1 máquina web completa con writeup de punta a punta.

**Referencia roadmap.sh:** Security skills, Web vulnerabilities, Programming/JavaScript solo lo necesario para XSS/DOM.

---

## Bloque 05 — Metodología, vulnerability assessment y reportes

**English summary:** Turn technical findings into professional methodology and reports.

**Objetivo:** Pasar de “resolver labs” a trabajar con metodología repetible.

**Por qué importa:** los empleadores no solo buscan exploits; buscan criterio, comunicación y reportes.

**Alcance:**
- Recon → scanning → exploitation → post-exploitation → reporting.
- Severidad, evidencia, impacto, reproducibilidad.
- Reporte ejecutivo vs técnico.
- Limpieza de datos sensibles.

**Entregables públicos:**
- `templates/report-template.md`
- `reports/` con reportes de práctica.
- `notes/07-methodology/`
- Checklist propio de engagement autorizado.

**Exit gate:**
- [ ] Tenés un reporte de práctica que alguien no técnico pueda leer.
- [ ] Cada finding tiene evidencia, impacto, reproducción y remediación.

**Referencia roadmap.sh:** Security fundamentals, risk/compliance solo lo necesario para reportar bien.

---

## Bloque 06 — Privilege escalation Linux/Windows

**English summary:** Practical privilege escalation with detection-aware notes.

**Objetivo:** Aprender rutas comunes de escalada y documentarlas con defensa.

**Por qué importa:** privesc es donde muchos perfiles junior se notan débiles.

**Alcance:**
- Linux: SUID, sudo, capabilities, cron, NFS, kernel, PATH, writable dirs.
- Windows: servicios, unquoted paths, DLL hijacking, tokens, UAC conceptos, registry, scheduled tasks.
- LinPEAS/WinPEAS, GTFOBins/LOLBAS.

**Entregables públicos:**
- `cheatsheets/linux-privesc.md`
- `cheatsheets/windows-privesc.md`
- `labs/privesc/`
- Notas de detección/mitigación por técnica.

**Exit gate:**
- [ ] Podés tomar una enumeración cruda y priorizar 3 vectores probables.
- [ ] Cada técnica documentada incluye cómo detectarla y mitigarla.

**Referencia roadmap.sh:** Operating systems, Security skills.

---

## Bloque 07 — Active Directory e internal pentesting

**English summary:** Active Directory fundamentals through authorized labs and documented attack paths.

**Objetivo:** Entender AD lo suficiente para explicar ataques comunes en entornos corporativos.

**Por qué importa:** muchos trabajos de pentesting/red team tocan AD directa o indirectamente.

**Alcance:**
- Windows para pentesters.
- Enumeración con rpcclient, ldapdomaindump, enum4linux-ng, BloodHound CE.
- Kerberoasting, AS-REP, LLMNR poisoning, NTLM relay, PtH/PtT.
- AD CS con Certipy.
- Lateral movement y persistencia conceptual en lab.

**Entregables públicos:**
- `notes/05-active-directory/`
- `labs/active-directory/`
- `scripts/ad-enum/` wrapper educativo.
- Diagrama de attack path sanitizado.

**Exit gate:**
- [ ] Un lab AD completo documentado con attack path y remediaciones.
- [ ] Podés explicar el riesgo sin depender de “magia” de herramientas.

**Referencia roadmap.sh:** Operating systems, Security skills, enterprise/internal security.

---

## Bloque 08 — Post-explotación, pivoting y C2 en lab

**English summary:** Controlled lab-only post-exploitation, pivoting, and C2 concepts.

**Objetivo:** Conocer post-explotación y C2 sin convertir el repo en una guía irresponsable.

**Por qué importa:** entender estas fases mejora reportes, detección y criterio ofensivo.

**Alcance:**
- Recolección de credenciales en lab.
- Pivoting con SSH y ligolo-ng.
- C2 open source en entorno controlado: Sliver o Mythic.
- OPSEC básico y ethics gates.

**Entregables públicos:**
- `notes/08-post-exploitation/`
- `labs/c2-lab/` con sanitización fuerte.
- Checklist de autorización y seguridad.
- Análisis defensivo: IOCs, logs, detecciones.

**Exit gate:**
- [ ] Todo C2/pivoting está claramente limitado a lab.
- [ ] Cada práctica incluye sección de detección y limpieza.

**Referencia roadmap.sh:** Security operations, red team concepts.

---

## Bloque 09 — Cloud security fundamentals

**English summary:** Cloud security basics focused on common misconfigurations and labs.

**Objetivo:** Sumar cloud básico sin dispersarse.

**Por qué importa:** muchos entornos reales son híbridos; cloud básico suma empleabilidad.

**Alcance:**
- IAM, buckets/storage, metadata, roles, políticas.
- Misconfiguraciones comunes.
- Labs gratuitos: flAWS.cloud, CloudGoat si el entorno lo permite.

**Entregables públicos:**
- `notes/09-cloud-security/`
- `labs/cloud/`
- Checklist de revisión de storage/IAM.

**Exit gate:**
- [ ] flAWS.cloud documentado con lecciones y mitigaciones.
- [ ] Podés explicar riesgos de IAM/storage sin humo.

**Referencia roadmap.sh:** Cloud skills/security.

---

## Bloque 10 — Go desde 0 para herramientas

**English summary:** Learn Go from zero after Python fundamentals, focused on fast security tooling.

**Objetivo:** Crear una herramienta rápida y portable en Go.

**Por qué importa:** Go es común en tooling moderno de seguridad por binarios únicos y concurrencia.

**Alcance:**
- Sintaxis base, módulos, errores.
- CLI con flags.
- Concurrencia con goroutines/channels.
- Networking y parsers.
- Tests básicos.

**Entregables públicos:**
- `scripts/go-scanner/` o herramienta equivalente.
- README con build, uso, benchmarks y comparación con Python.

**Exit gate:**
- [ ] Herramienta Go funcional con tests y binario documentado.
- [ ] Explicás cuándo elegir Go vs Python.

**Referencia roadmap.sh:** Programming Skills / Go.

---

## Bloque 11 — Detección y defensa para pensar como blue team

**English summary:** Add detection literacy so offensive work becomes professionally credible.

**Objetivo:** No solo atacar: saber cómo se detecta y se mitiga.

**Por qué importa:** diferencia un writeup amateur de un perfil empleable.

**Alcance:**
- Logs relevantes Windows/Linux/web.
- IOCs básicos.
- Detecciones para técnicas estudiadas.
- MITRE ATT&CK como lenguaje común.

**Entregables públicos:**
- `notes/10-detection/`
- `cheatsheets/detection.md`
- Mapeo ATT&CK de writeups seleccionados.

**Exit gate:**
- [ ] Al menos 5 técnicas tienen mapeo ataque → evidencia → detección → mitigación.

**Referencia roadmap.sh:** Security operations / defense.

---

## Bloque 12 — Portfolio final, entrevistas y búsqueda laboral

**English summary:** Convert the repository into a job-hunting asset.

**Objetivo:** Convertir el estudio en empleabilidad real.

**Por qué importa:** el repo solo sirve si está narrado para reclutadores y entrevistas técnicas.

**Alcance:**
- Curaduría de mejores writeups.
- README final bilingüe.
- CV técnico y LinkedIn.
- Simulacros de entrevista.
- Mapeo de ofertas LATAM/remotas.

**Entregables públicos:**
- README final pulido.
- `roadmap/progress.md` completo.
- 3 writeups destacados.
- 2-3 posts técnicos.
- CV técnico.

**Exit gate:**
- [ ] Un reclutador entiende tu nivel en 2 minutos.
- [ ] Un técnico encuentra evidencia profunda en 10 minutos.
- [ ] Tenés respuestas preparadas para cada writeup destacado.

**Referencia roadmap.sh:** career/job prep, no técnica.
