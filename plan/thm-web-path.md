# Path adaptado: Web Application Pentesting (TryHackMe) — cuenta FREE

> Estado verificado el 2026-07-23 vía API autenticada (`/api/v2/rooms/details?roomCode=X`,
> campo `freeToUse` / mensaje "The room is subscriber only.").
> 10 de 34 rooms son gratuitas. Las bloqueadas se cubren con PortSwigger Academy (100% gratis).

## Progreso

| Fecha | Room | Writeup |
|---|---|---|
| 2026-07-24 | ✅ Enumeration & Brute Force | labs/tryhackme/enumeration-bruteforce.md |

## Mapa FREE / LOCK por módulo

### 1. Authentication
| Estado | Room | URL |
|---|---|---|
| ✅ FREE (hecha) | Enumeration & Brute Force | https://tryhackme.com/room/enumerationbruteforce |
| LOCK | Session Management | https://tryhackme.com/room/sessionmanagement |
| LOCK | JWT Security | https://tryhackme.com/room/jwtsecurity |
| LOCK | OAuth Vulnerabilities | https://tryhackme.com/room/oauthvulnerabilities |
| LOCK | Multi-Factor Authentication | https://tryhackme.com/room/multifactorauthentications |
| LOCK | Hammer (challenge) | https://tryhackme.com/room/hammer |

### 2. Injection Attacks
| Estado | Room | URL |
|---|---|---|
| FREE | Advanced SQL Injection | https://tryhackme.com/room/advancedsqlinjection |
| FREE | NoSQL Injection | https://tryhackme.com/room/nosqlinjectiontutorial |
| LOCK | XXE Injection | https://tryhackme.com/room/xxeinjection |
| LOCK | Server-side Template Injection | https://tryhackme.com/room/serversidetemplateinjection |
| LOCK | LDAP Injection | https://tryhackme.com/room/ldapinjection |
| LOCK | ORM Injection | https://tryhackme.com/room/orminjection |
| LOCK | Injectics (challenge) | https://tryhackme.com/room/injectics |

### 3. Advanced Server-Side Attacks
| Estado | Room | URL |
|---|---|---|
| FREE | Insecure Deserialisation | https://tryhackme.com/room/insecuredeserialisation |
| FREE | SSRF | https://tryhackme.com/room/ssrfhr |
| LOCK | File Inclusion, Path Traversal | https://tryhackme.com/room/filepathtraversal |
| LOCK | Race Conditions | https://tryhackme.com/room/raceconditionsattacks |
| LOCK | Prototype Pollution | https://tryhackme.com/room/prototypepollution |
| LOCK | Include (challenge) | https://tryhackme.com/room/include |

### 4. Advanced Client-Side Attacks
| Estado | Room | URL |
|---|---|---|
| FREE | XSS | https://tryhackme.com/room/axss |
| FREE | CSRF | https://tryhackme.com/room/csrfV2 |
| LOCK | DOM-Based Attacks | https://tryhackme.com/room/dombasedattacks |
| LOCK | CORS & SOP | https://tryhackme.com/room/corsandsop |
| LOCK | Whats Your Name? (challenge) | https://tryhackme.com/room/whatsyourname |

### 5. HTTP Request Smuggling
| Estado | Room | URL |
|---|---|---|
| FREE | HTTP Request Smuggling | https://tryhackme.com/room/httprequestsmuggling |
| FREE | HTTP/2 Request Smuggling | https://tryhackme.com/room/http2requestsmuggling |
| LOCK | Request Smuggling: WebSockets | https://tryhackme.com/room/wsrequestsmuggling |
| LOCK | HTTP Browser Desync | https://tryhackme.com/room/requestsmugglingbrowserdesync |
| LOCK | El Bandito (challenge) | https://tryhackme.com/room/elbandito |

### 6. Web Frameworks
| Estado | Room | URL |
|---|---|---|
| FREE | Web Frameworks: Code Review | https://tryhackme.com/room/webframeworkscodereview |
| LOCK | Web Frameworks: Java | https://tryhackme.com/room/webframeworksjava |
| LOCK | Web Frameworks: Python | https://tryhackme.com/room/webframeworkspython |
| LOCK | Web Frameworks: .NET | https://tryhackme.com/room/webframeworksnet |
| LOCK | Source Code Review: PHP | https://tryhackme.com/room/sourcecodereviewsphp |

## Orden de estudio asignado (gratis, alineado a Fase 2 del plan 2026)

1. **Enumeration & Brute Force** (THM) — recon + auth básica
2. **CSRF** (THM, `/room/csrfV2`) — cierra la deuda; después volver al lab
   de PortSwigger "SameSite Lax bypass via cookie refresh" y resolverlo
3. **XSS** (THM)
4. **Advanced SQL Injection** (THM)
5. **NoSQL Injection** (THM)
6. **SSRF** (THM)
7. **Insecure Deserialisation** (THM)
8. **HTTP Request Smuggling** + **HTTP/2 Request Smuggling** (THM) — stretch
9. **Web Frameworks: Code Review** (THM) — cierre del bloque

## Equivalencias gratuitas para rooms LOCK (PortSwigger Academy, todo gratis)

| Room LOCK | Topic PortSwigger |
|---|---|
| Session Management / JWT / OAuth / MFA | Authentication, JWT attacks, OAuth authentication |
| XXE Injection | XXE injection |
| SSTI | Server-side template injection |
| LDAP Injection | LDAP injection |
| File Inclusion, Path Traversal | Path traversal + File upload vulnerabilities |
| Race Conditions | Race conditions |
| Prototype Pollution | Prototype pollution |
| DOM-Based Attacks / CORS & SOP | DOM-based vulnerabilities, CORS |
| WS Request Smuggling / Browser Desync | Request smuggling (advanced labs) |
| Frameworks Java/Python/.NET/PHP | (difiere — code review se practica con repos propios) |

## Reglas

- Writeups en `labs/tryhackme/<room>.md` con formato repaso: técnica, request clave,
  por qué funciona, errores comunes. Sin flags ni respuestas literales.
- Cada room FREE completada desbloquea la siguiente de la lista.
- Challenges LOCK quedan como deuda hasta tener Premium (o se simulan con
  máquinas VulnHub/HTB retiradas equivalentes).
