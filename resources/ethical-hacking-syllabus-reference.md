# Temario de referencia — Hacking Ético

> Este es un temario típico de cursos de hacking ético universitarios (incluyendo referencias al estilo UTN / cursos de ethical hacking). Sirve para verificar que el plan de estudios cubre todos los temas clave.

## 1. Fundamentos y Marco Legal
- Conceptos de seguridad informática: confidencialidad, integridad, disponibilidad.
- Diferencia entre hacker, cracker, pentester, red team, blue team.
- Marco legal y ético: autorización, scope, contratos, leyes de protección de datos.
- Metodologías: PTES, OWASP Testing Guide, NIST SP 800-115, MITRE ATT&CK.

## 2. Linux para Pentesters
- Comandos esenciales, manejo de permisos, pipes, redirecciones.
- Bash scripting.
- Administración de usuarios y grupos.
- Administración de servicios y redes en Linux.

## 3. Redes y Protocolos
- Modelo OSI y TCP/IP.
- Protocolos: TCP, UDP, IP, ICMP, DNS, HTTP/HTTPS, ARP.
- Subnetting y enrutamiento básico.
- Captura y análisis de tráfico (Wireshark, tcpdump).
- Escaneo de redes y puertos (Nmap, Masscan).

## 4. Sistemas Windows y Active Directory
- Arquitectura Windows, registros, servicios, SAM, LSASS.
- Usuarios, grupos, privilegios y UAC.
- Conceptos de Active Directory: dominios, árboles, bosques, trusts, GPOs.
- Enumeración de AD.
- Ataques comunes de AD: Kerberoasting, AS-REP Roasting, LLMNR poisoning, Pass-the-Hash, NTLM relay.

## 5. Web Application Pentesting
- Arquitectura web y protocolo HTTP.
- OWASP Top 10.
- SQL Injection, XSS, CSRF, SSRF, XXE, Command Injection, Path Traversal, LFI/RFI.
- Inseguridad en autenticación y autorización (IDOR, broken access control).
- Subida de archivos insegura.
- Uso de proxies: Burp Suite, OWASP ZAP.

## 6. Explotación de Vulnerabilidades
- Fases del pentest: reconocimiento, escaneo, explotación, post-explotación, reporte.
- Búsqueda de exploits (Exploit-DB, searchsploit, CVEs).
- Uso de frameworks: Metasploit.
- Creación de payloads básicos.

## 7. Post-Explotación
- Escalada de privilegios en Linux y Windows.
- Persistencia: scheduled tasks, services, registry, cron.
- Recolección de credenciales: Mimikatz, LaZagne, hashes.
- Pivoting y tunneling.
- Exfiltración de datos.
- Antiforense y limpieza de logs (con fines defensivos).

## 8. Ingeniería Social y Phishing
- Técnicas de ingeniería social.
- Phishing, spear-phishing, vishing, smishing.
- Herramientas de phishing: GoPhish, EvilGoPhish, SET.
- Concientización y medidas de mitigación.

## 9. Wireless Pentesting (opcional)
- Protocolos Wi-Fi (WEP, WPA/WPA2, WPA3).
- Ataques a redes inalámbricas.
- Mitigaciones.

## 10. Reporte y Comunicación
- Estructura de un reporte técnico.
- Clasificación de severidad (CVSS).
- Recomendaciones y remediación.
- Comunicación con clientes técnicos y no técnicos.

## 11. Hacking Ético en la Nube (opcional)
- Conceptos de AWS/Azure/GCP.
- S3 buckets públicos, IAM misconfigs.
- flAWS / CloudGoat como práctica.

## Uso de este documento

- Marcar cada tema con [x] cuando se estudie y practique.
- Cruzar con el plan de `plan/2026-redteam-plan.md`.
- Agregar links a notas de cada tema en `notes/`.
