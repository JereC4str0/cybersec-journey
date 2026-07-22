# Progreso del roadmap mastery-based

> Regla: marcar un bloque como completo solo cuando la exit gate está cumplida y la evidencia pública está linkeada.

## Estado actual

- Bloque actual sugerido: **05 — Metodología (primera máquina: Kioptrix L1)**.
- Bloque 02 (Networking): exit gate completa el 2026-07-21 (notas 01-04).
- Sesiones de mentoría:
  - `roadmap/sessions/001-inicio-evidencia-python.md` — scaffold provisto; micro-cambios en pausa.
  - `roadmap/sessions/002-networking-nmap.md` — completa (notas 01-04).
  - `roadmap/sessions/003-nse-primera-maquina.md` — ACTIVA (Parte A hecha; Parte B: lab Kioptrix).
- Evidencia ya existente:
  - [x] OverTheWire Bandit 0-32: `labs/overthewire/bandit/`
  - [x] Scaffold inicial de port scanner provisto por mentoría: `scripts/port-scanner/`
  - [ ] Notas de networking pendientes (sesión 002).
  - [ ] Primer writeup de máquina vulnerable pendiente.

## Checklist de bloques

- [ ] Bloque 00 — Sistema de evidencia pública
- [ ] Bloque 01 — Linux y Git para trabajo de seguridad
- [x] Bloque 02 — Networking para pentesting (exit gate 2026-07-21: notas 01-04, cheatsheet nmap)
- [ ] Bloque 03 — Python desde 0 para security tooling
- [ ] Bloque 04 — Web security y API testing
- [ ] Bloque 05 — Metodología, vulnerability assessment y reportes
- [ ] Bloque 06 — Privilege escalation Linux/Windows
- [ ] Bloque 07 — Active Directory e internal pentesting
- [ ] Bloque 08 — Post-explotación, pivoting y C2 en lab
- [ ] Bloque 09 — Cloud security fundamentals
- [ ] Bloque 10 — Go desde 0 para herramientas
- [ ] Bloque 11 — Detección y defensa para pensar como blue team
- [ ] Bloque 12 — Portfolio final, entrevistas y búsqueda laboral

## Próximos entregables concretos

1. `templates/writeup-template.md`
2. `templates/report-template.md`
3. `scripts/port-scanner/` v1.0
4. `notes/02-networking/`
5. `cheatsheets/nmap.md`
6. Primer writeup de máquina vulnerable

## Notas

- No usar fechas como gate.
- Cada commit debe contar una historia pequeña: qué se aprendió, qué se construyó o qué se documentó.
- Todo ejemplo ofensivo debe indicar entorno autorizado y mitigación.
