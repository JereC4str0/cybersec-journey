# Plan de Estudios 2026 — Red Team / Pentesting (autodidacta, gratis, práctico)

> **Goal:** Llegar a fin de año con un portfolio sólido y conocimientos prácticos de pentesting/red team para buscar trabajo, sin pagar certificaciones.
>
> **Assumptions:** Base de desarrollador, conocimiento previo de Linux, 4-5 horas/día de estudio, presupuesto $0.
>
> **Tech Stack de apoyo:** Python, Bash, Markdown, Git, Burp Suite Community, impacket, BloodHound CE.

---

## Fase 1: Fundamentos (Semanas 1-2)

**Objetivo:** Reforzar redes, Linux y scripting para que el resto del camino sea más fácil.

### Semana 1 — Networking + Linux + Metodología
- **Teoría:** Modelo OSI/TCP-IP, protocolos (TCP, UDP, HTTP, DNS, ICMP), subnetting básico, escaneo de puertos, handshake.
- **Práctica:**
  - OverTheWire Bandit (todos los niveles).
  - Nmap básico en máquinas locales/VulnHub.
- **Script:** Port scanner en Python (TCP connect scan básico).
- **Documentar:** Notas de networking en `notes/02-networking/`.

### Semana 2 — Scripting + Git + Flujo de trabajo
- **Teoría:** Python para red, requests, sockets, regex, manejo de argumentos (`argparse`).
- **Práctica:**
  - Mejorar port scanner: banners, thread pool, escaneo de rangos.
  - Automatizar un pequeño enumerador de servicios HTTP.
- **Documentar:** Subir scripts a `scripts/port-scanner/` con README.

---

## Fase 2: Web Application Pentesting (Semanas 3-7)

**Objetivo:** Dominar OWASP Top 10 a nivel práctico y documentar writeups.

### Semana 3 — Burp Suite + Information Gathering
- Instalar y configurar Burp Suite Community.
- Aprender proxy, repeater, intruder (limitado en Community).
- Labs de PortSwigger: Information Gathering.

### Semana 4 — SQL Injection & XSS
- PortSwigger: SQLi (básica, blind, UNION) y XSS (reflected, stored, DOM).
- Practicar en DVWA o máquina de VulnHub.
- **Script:** Detector simple de parámetros potencialmente inyectables (GET) en Python.

### Semana 5 — Authentication & Authorization
- PortSwigger: Autenticación, autorización, IDOR, broken access control.
- Probar brute-force controlado con hydra/Burp.
- **Script:** Fuzzer de rutas/directorios web (básico) en Python.

### Semana 6 — File Upload, SSRF, XXE, Command Injection
- PortSwigger: file upload, SSRF, XXE, OS command injection.
- VulnHub: máquina fácil tipo RickdiculouslyEasy o Mr. Robot.
- **Documentar:** Primer writeup completo en `labs/vulnhub/`.

### Semana 7 — Consolidación Web + API testing + Máquina HTB fácil
- Resolver 1 máquina “Easy” de HackTheBox (gratuita).
- PortSwigger: labs de API testing (recon de endpoints, métodos HTTP, mass assignment). Las APIs son hoy el vector dominante en aplicaciones reales.
- Completar reporte de la máquina con metodología.
- **Proyecto:** Web fuzzer/dirbuster en Python, versión 1.0.

---

## Fase 3: Active Directory & Internal Pentesting (Semanas 8-12)

**Objetivo:** Entender Windows, AD y los ataques más comunes en entornos corporativos.

### Semana 8 — Windows para Pentesters
- Estructura de Windows, SAM/LSASS, usuarios/grupos, UAC, firewall.
- PowerShell básico para pentesting.
- Herramientas: impacket, NetExec (`nxc`, sucesor mantenido de CrackMapExec, que está archivado desde 2023), evil-winrm.

### Semana 9 — Enumeración de AD
- BloodHound CE (gratuito), SharpHound.
- Enumeración con ldapdomaindump, enum4linux-ng, rpcclient.
- **Documentar:** Notas en `notes/05-active-directory/`.

### Semana 10 — Ataques de AD clásicos
- Kerberoasting, AS-REP Roasting, LLMNR/NBT-NS poisoning con Responder.
- AD CS (Active Directory Certificate Services): enumeración y abuso con Certipy (ESC1-ESC8). Hoy es uno de los vectores más explotados en entornos corporativos reales.
- Coerción de autenticación (PetitPotam/PrinterBug con Coercer) y NTLM relay moderno (krbrelayx).
- Pass-the-Hash, Pass-the-Ticket.
- Labs gratuitos de AD en TryHackMe: “Active Directory Basics”, “Active Directory Enumeration & Attacks”.

### Semana 11 — Lateral Movement + Persistencia
- WMI, PsExec, scheduled tasks, remote services.
- Persistencia básica: Golden/Silver ticket (concepto), ACL abuse.
- **Script:** Wrapper de impacket para automatizar enumeración.

### Semana 12 — Máquina de AD gratuita
- VulnHub: máquina con AD (ej. “VulnAD”, “Active Directory Lab” o similar).
- Documentar writeup completo.

---

## Fase 4: Privilege Escalation (Semanas 13-16)

**Objetivo:** Aprender a escalar privilegios en Linux y Windows.

### Semana 13 — Linux Privilege Escalation
- LinPEAS, GTFOBins, SUID, capabilities, cron, kernel exploits, sudo misconfigs.
- Máquinas de VulnHub/HTB enfocadas en Linux PE.
- **Documentar:** Cheatsheet Linux PE.

### Semana 14 — Windows Privilege Escalation
- WinPEAS, service misconfigs, unquoted paths, DLL hijacking, token impersonation, UAC bypass (conceptos).
- Máquina Windows en TryHackMe/VulnHub.

### Semana 15 — Post-explotación
- Recolección de credenciales (Mimikatz, LaZagne, nanodump).
- Exfiltración segura: dnscat2 concepto, goshs, cloakify.
- Pivoting básico con SSH tunneling y ligolo-ng (gratuito).

### Semana 16 — C2 y Report Writing
- Instalar y probar un C2 open source: Sliver (muy activo, commits semanales) o Mythic. Havoc está archivado: conocerlo está bien, pero no conviene apostar a tooling sin mantenimiento.
- Práctica: generar payload, ejecutar en lab, capturar sesión.
- **Documentar:** Template de reporte de pentesting.

---

## Fase 5: Proyectos + Máquinas variadas (Semanas 17-20)

**Objetivo:** Acumular evidencia y pulir herramientas propias.

- Resolver 1-2 máquinas por semana de HTB/VulnHub/Proving Grounds Play.
- Fundamentos de cloud security: flAWS.cloud y CloudGoat (AWS, gratis). Los entornos híbridos cloud/on-prem son el default en 2026.
- Opcional (stretch): labs de LLM security de PortSwigger, por si te interesa el nicho de AI red teaming.
- Mejorar scripts: web fuzzer, port scanner, enumerador de AD.
- Crear un **generador de reportes** en Markdown/HTML para tus writeups.
- Empezar a publicar writeups (puedes mantenerlos en este repo).

---

## Fase 6: Portfolio & Job Prep (Semanas 21-24)

**Objetivo:** Convertir tu estudio en algo presentable a empleadores.

- Pulir README del repo.
- Crear un CV técnico enfocado en pentesting.
- Escribir 2-3 posts/blog entries explicando técnicas que dominaste.
- Simulacro de entrevista técnica.
- Networking: LinkedIn, Discord de comunidades hispanas (Hack4u, HackTheBox, etc.).
- Revisar ofertas laborales y mapear requisitos vs. lo que sabes.

---

## Milestones / Evidencias clave

- [ ] Port scanner propio en Python
- [ ] Web fuzzer/dirbuster propio en Python
- [ ] 30+ labs de PortSwigger resueltos
- [ ] 10+ máquinas vulnerable resueltas con writeups
- [ ] 1 máquina/lab de AD completo documentado
- [ ] 1 ataque de AD CS documentado (Certipy)
- [ ] 1 lab de API testing documentado
- [ ] flAWS.cloud completado (cloud básico)
- [ ] Cheatsheets de Linux PE, Windows PE, AD, Web
- [ ] Generador de reportes de pentesting
- [ ] 2-3 posts/blog explicando técnicas

---

## Recursos gratuitos por fase

| Fase | Recursos |
|------|----------|
| Fundamentos | OverTheWire Bandit, Cisco Skills for All (Networking), Nmap docs |
| Web | PortSwigger, DVWA, bWAPP, Web Security Academy |
| AD | TryHackMe AD rooms, VulnHub AD labs, BloodHound CE docs, impacket docs |
| PE | HackTricks PE sections, GTFOBins, PayloadsAllTheThings |
| C2 | Sliver, Mythic, Metasploit (gratuito) |
| Cloud | flAWS.cloud, CloudGoat, HackTricks Cloud |
| Job prep | LinkedIn, comunidades, simulacros con ChatGPT/Hermes |

---

## Notas finales

- **No pagues certificaciones por ahora.** Tu portfolio (repo, writeups, scripts) hablará por ti.
- **Aprende haciendo:** cada semana debe terminar con algo concreto: un script, un writeup o una máquina.
- **Documenta todo:** la documentación es parte del trabajo del pentester.
- **Sé ético:** todos los labs deben hacerse en entornos autorizados o de práctica.
- **Pensá como atacante, documentá como defensor:** por cada técnica, anotá cómo se detecta y cómo se mitiga. Eso es lo que diferencia un writeup de un reporte profesional.
