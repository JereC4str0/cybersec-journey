# Semana 2: Scripting, Git y Flujo de Trabajo

> **Objetivo semanal:** Convertir el port scanner de la semana 1 en una herramienta seria (concurrencia, banners, output estructurado) y crear tu segundo script: un enumerador de servicios HTTP. Además, dejar un flujo de trabajo de Git limpio y reproducible.
>
> **Carga diaria:** 4-5 horas totales.
> **Distribución recomendada:** 1.5h teoría + 2.5h práctica + 1h documentación/revisión.
> **Entregable final de semana:** `scripts/port-scanner/` v2.0 y `scripts/enumerators/http-enum.py` con README y tests, todo commiteado.
>
> **Prerequisito:** port scanner v1.0 de la semana 1 (si quedó pendiente, los días 1-2 sirven para cerrarlo).

---

## Día 1 — Entorno Python moderno + refactor del port scanner

### Teoría (1.5h)
- [ ] Entornos virtuales y gestión de proyectos con `uv` (ya lo tenés instalado).
- [ ] Estructura de proyecto: `pyproject.toml`, separación CLI/lógica, `if __name__ == "__main__"`.
- [ ] Type hints básicos y por qué importan en herramientas que crecen.

**Recursos:**
- [uv docs](https://docs.astral.sh/uv/)
- [Python typing cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

### Práctica (2.5h)
- [ ] Inicializar el proyecto: `uv init` en `scripts/port-scanner/` (o migrar el existente).
- [ ] Refactor: separar el scanner en funciones puras (`scan_port`, `scan_host`) y capa CLI.
- [ ] Agregar type hints a las funciones principales.

### Documentación (1h)
- [ ] Actualizar `scripts/port-scanner/README.md`: instalación con `uv`, uso, ejemplos.
- [ ] Notas en `notes/03-scripting/01-python-packaging.md`.

### Desafío del día
> Que `uv run portscanner -t 127.0.0.1 -p 1-1024` funcione desde un clone limpio del repo sin instalar nada a mano.

---

## Día 2 — Concurrencia real: de threads a ThreadPoolExecutor

### Teoría (1.5h)
- [ ] GIL: qué es y por qué para I/O-bound (sockets) los threads sí sirven.
- [ ] `concurrent.futures.ThreadPoolExecutor` y `as_completed`.
- [ ] Rate limiting y timeouts: por qué un scanner sin control tumba servicios (y te delata).

**Recursos:**
- [Real Python: concurrency](https://realpython.com/python-concurrency/)
- `python3 -c "import concurrent.futures; help(concurrent.futures.ThreadPoolExecutor)"`

### Práctica (2.5h)
- [ ] Reemplazar el manejo manual de threads por `ThreadPoolExecutor` con `--threads` configurable.
- [ ] Agregar barra de progreso simple (contador) o `rich` si querés probarla.
- [ ] Medir: escanear 1-65535 local antes y después del refactor; anotar tiempos.

### Documentación (1h)
- [ ] Notas en `notes/03-scripting/02-concurrencia.md` con los benchmarks.

### Desafío del día
> Escaneo full-range (65535 puertos) contra localhost en menos de 60 segundos sin falsos positivos.

---

## Día 3 — Banner grabbing y detección de servicios

### Teoría (1.5h)
- [ ] Qué es un banner y qué servicios lo exponen (SSH, FTP, SMTP, HTTP).
- [ ] HTTP: parsear `Server`, status codes, redirects.
- [ ] Por qué los banners mienten (y cómo lo usan los admins para despistar).

### Práctica (2.5h)
- [ ] Agregar banner grabbing al scanner con timeout corto (1-2s) y manejo de errores.
- [ ] Detectar al menos: SSH, FTP, HTTP (con título de página si responde HTML).
- [ ] Output dual: tabla legible por consola + JSON/CSV con `--output`.

### Documentación (1h)
- [ ] Ejemplos de salida en el README (con datos de lab, no de terceros).

### Desafío del día
> Levantar 3 servicios locales (ej. `python3 -m http.server`, SSH, un netcat listener) y que el scanner los identifique correctamente a los 3.

---

## Día 4 — Segundo script: enumerador HTTP

### Teoría (1.5h)
- [ ] Requests HTTP con `httpx` o `requests`: headers, métodos, TLS.
- [ ] Qué enumera un pentester primero: título, servidor, tecnologías, rutas comunes, robots.txt.

**Recursos:**
- [httpx docs](https://www.python-httpx.org/)

### Práctica (2.5h)
- [ ] Crear `scripts/enumerators/http-enum.py`: dado un host/URL, reporta status, headers, título, server, redirect chain y contenido de robots.txt.
- [ ] Aceptar lista de hosts por archivo (`-l hosts.txt`) y concurrencia.
- [ ] Manejar HTTPS con certificados autofirmados (flag `-k`).

### Documentación (1h)
- [ ] `scripts/enumerators/README.md` con uso y ejemplos.

### Desafío del día
> Correr el enumerador contra una máquina VulnHub/HTB de práctica y extraer información útil para un hipotético recon.

---

## Día 5 — Git workflow y calidad de código

### Teoría (1.5h)
- [ ] Commits atómicos y mensajes tipo conventional commits (`feat:`, `fix:`, `docs:`).
- [ ] `.gitignore` bien hecho para herramientas (outputs, venvs, capturas).
- [ ] Pre-commit hooks básicos (opcional: `ruff` para lint).

### Práctica (2.5h)
- [ ] Revisar el historial del repo: reescribir nada, pero de ahora en más commits atómicos.
- [ ] Agregar `ruff` al proyecto y dejar el código limpio (`uv run ruff check .`).
- [ ] Configurar `.gitignore` global del repo para `*.json`, `*.csv` de outputs, `.venv/`.

### Documentación (1h)
- [ ] Notas en `notes/03-scripting/03-git-workflow.md` con tu convención de commits.

### Desafío del día
> Hacer al menos 4 commits atómicos hoy, cada uno con un solo cambio lógico y mensaje claro.

---

## Día 6 — Tests y robustez

### Teoría (1.5h)
- [ ] `pytest`: fixtures, parametrize, mocks de red (no testear contra internet real).
- [ ] Qué testear en una herramienta ofensiva: parseo de args, manejo de errores, formato de output.

### Práctica (2.5h)
- [ ] Tests del port scanner: puerto abierto/cerrado simulado con sockets locales, rangos inválidos, output JSON válido.
- [ ] Tests del enumerador HTTP con `pytest-httpx` o un servidor de test local.
- [ ] Que `uv run pytest` pase entero desde un clone limpio.

### Documentación (1h)
- [ ] Sección "Testing" en ambos READMEs.

### Desafío del día
> Cobertura razonable (>70%) en la lógica de scan, medida con `pytest --cov` (opcional).

---

## Día 7 — Cierre, integración y push

### Teoría (1h)
- [ ] Leer el código de una herramienta real chica (ej. `fierce` o un fuzzer simple en GitHub) y anotar 3 ideas para robar.

### Práctica (2h)
- [ ] Pipeline completo: escanear una VM de lab con el port scanner → pasar los servicios web encontrados al enumerador HTTP → guardar todo en JSON.
- [ ] Ese flujo manual de hoy es el boceto del automatizador de la Fase 2: dejarlo anotado.

### Documentación (1-2h)
- [ ] Resumen de la semana en `notes/00-fundamentos/semana-02-resumen.md`.
- [ ] Actualizar `labs/tracking.md` y el README principal.
- [ ] Commit y push final.

### Desafío final de la semana
> Que otra persona pueda clonar el repo, seguir los READMEs y usar ambas herramientas sin preguntarte nada.

---

## Checklist de entregables de la semana

- [ ] `scripts/port-scanner/` v2.0: concurrencia, banners, JSON/CSV, tests.
- [ ] `scripts/enumerators/http-enum.py` funcional con README.
- [ ] Proyecto gestionado con `uv`, lint limpio con `ruff`.
- [ ] Notas de scripting en `notes/03-scripting/`.
- [ ] `labs/tracking.md` y README actualizados.
- [ ] Commits atómicos durante toda la semana.

---

## Recordatorios

- **Solo escaneás lo que controlás o tenés autorización escrita para escanear.**
- **Un scanner agresivo sin rate limit puede tumbar servicios: en lab aprendé a controlarlo, en producción te puede costar el trabajo.**
- **Documentá decisiones de diseño, no solo comandos: eso es lo que un empleador quiere leer.**
