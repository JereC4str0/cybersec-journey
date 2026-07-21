# Mentoría 001 — Inicio de evidencia pública + Python security tooling

> Modalidad: mastery-based. No hay fecha límite. La sesión se cierra cuando los entregables están completos y documentados.

## Situación actual

- Ya tenés Bandit 0-32 documentado en `labs/overthewire/bandit/`.
- El roadmap nuevo está en `roadmap/`.
- Próximo paso útil: convertir tu base Linux/Git en evidencia profesional y arrancar Python desde 0 con una herramienta real.

## Objetivo del bloque/tema

Desbloquear la capacidad de producir evidencia pública con calidad profesional: templates, notas, cheatsheets y una primera herramienta Python ejecutable.

## Teoría (alcance)

No hace falta curso completo todavía. Necesitás entender lo suficiente para explicar:

1. Qué es un puerto TCP y qué significa “abierto/cerrado/filtrado”.
2. Qué hace Nmap con `-sV`, `-sC`, `-oA`.
3. Qué es un socket TCP y por qué `connect_ex` devuelve 0 cuando el puerto está abierto.
4. Qué hace `argparse` y por qué una CLI clara importa en herramientas de seguridad.
5. Qué debe tener un writeup/reporte para que un empleador lo tome en serio.

## Práctica (entregable)

### Tarea 1 — Templates profesionales

Crear:

- `templates/writeup-template.md`
- `templates/report-template.md`

Requisitos mínimos del writeup:

- Contexto autorizado del lab.
- Objetivo.
- Enumeración.
- Explotación.
- Privesc si aplica.
- Evidencia sanitizada.
- Detección.
- Mitigación.
- Lecciones.

Requisitos mínimos del reporte:

- Resumen ejecutivo.
- Alcance y autorización.
- Hallazgos con severidad.
- Evidencia.
- Reproducción.
- Impacto.
- Remediación.
- Anexo técnico.

### Tarea 2 — Port scanner v0.1 con scaffold guiado

Como estás aprendiendo Python desde 0, no arrancás desde una página en blanco. Ya dejé un scaffold runnable en:

- `scripts/port-scanner/portscanner.py`
- `scripts/port-scanner/README.md`
- `scripts/port-scanner/.gitignore`

Tu trabajo es usarlo como andamio de aprendizaje:

1. Correrlo sin modificar nada.
2. Identificar dónde están `argparse`, `parse_port_range()`, `scan_port()` y `main()`.
3. Hacer micro-cambios guiados del README:
   - cambiar timeout,
   - imprimir cantidad de puertos revisados,
   - agregar `--show-closed` con pista.
4. Documentar lo aprendido en `notes/03-scripting/01-python-scaffold.md`.

Versión mínima a probar:

```bash
python3 scripts/port-scanner/portscanner.py -t 127.0.0.1 -p 1-1024
```

Formato repaso:

```bash
mkdir -p scripts/port-scanner && cd scripts/port-scanner && uv init --app
```

- Comando: `uv init --app`
- Concepto: crea proyecto Python moderno con `pyproject.toml`.
- Uso real: herramientas reproducibles que otros pueden clonar y correr.
- Error común: meter outputs, venvs o credenciales en git.
- Variante: si no querés `uv` todavía, hacelo con Python stdlib puro primero.

```bash
nmap -sV -sC -oA localhost-scan 127.0.0.1
```

- Comando: `nmap -sV -sC -oA localhost-scan 127.0.0.1`
- Concepto: detección de servicios + scripts por defecto + exportación de evidencia.
- Uso real: baseline de recon en un engagement autorizado.
- Error común: escanear objetivos sin autorización o publicar outputs con datos sensibles.
- Variante: `-p-` para todos los puertos solo en lab propio.

### Tarea 3 — Notas de networking iniciales

Crear:

- `notes/02-networking/01-osi-tcpip.md`
- `notes/02-networking/03-nmap-localhost.md`
- `cheatsheets/nmap.md`

Contenido mínimo:

- OSI/TCP-IP explicado con ejemplos de pentesting.
- 10 comandos Nmap explicados en formato repaso.
- Evidencia localhost sanitizada: qué puertos aparecen, qué servicios, qué riesgo tendrían si estuvieran expuestos.

### Tarea 4 — Tracking público

Actualizar `labs/tracking.md` con una fila para esta sesión:

- Plataforma: Local/lab autorizado
- Máquina/Lab: localhost + port scanner v0.1
- Técnicas: TCP sockets, Nmap básico, documentación
- Estado: pendiente hasta completar

## Desafío

Si terminás los cambios guiados rápido, subí a v0.2 con ayuda:

- agregar `ThreadPoolExecutor` copiando un ejemplo pequeño,
- agregar `--threads`,
- comparar tiempo de escaneo con 1 vs 50 threads contra localhost,
- documentar el benchmark en `notes/03-scripting/02-concurrencia.md`.

Si `ThreadPoolExecutor` todavía se siente grande, no bloquea: se deja para la próxima sesión.

## Entregable público

Para cerrar la sesión necesito ver en el repo:

1. `templates/writeup-template.md`
2. `templates/report-template.md`
3. `scripts/port-scanner/portscanner.py`
4. `scripts/port-scanner/README.md`
5. `notes/02-networking/01-osi-tcpip.md`
6. `notes/02-networking/03-nmap-localhost.md`
7. `cheatsheets/nmap.md`
8. `labs/tracking.md` actualizado
9. Commits chicos y claros, idealmente 3-6 commits separados.

## Criterios de revisión

Voy a revisar:

- ¿Puedo clonar y ejecutar el scanner sin adivinar pasos?
- ¿La documentación explica qué hace, cuándo usarlo y cómo defenderse?
- ¿No hay credenciales, IPs sensibles ni outputs innecesarios?
- ¿Los commits cuentan una historia clara?
- ¿La práctica quedó limitada a entorno autorizado?

## Pregunta de seguimiento

Cuando termines, pasame:

- el commit o rama donde quedó,
- la salida de `python3 portscanner.py -t 127.0.0.1 -p 1-1024`,
- el comando Nmap que usaste,
- qué parte te costó más.

Con eso analizamos resultados y ajustamos la siguiente mentoría.
