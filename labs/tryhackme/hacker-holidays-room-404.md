# Writeup: TryHackMe — Hacker Holidays 2026: Room 404

## Información
- **Plataforma:** TryHackMe
- **Evento:** Hacker Holidays 2026 — The Byte Lotus
- **Room:** Room 404
- **Tema:** Web / Directory Enumeration / Git Exposure
- **Dificultad:** Very Easy
- **Fecha:** 2026-08-07

## Resumen ejecutivo

Room de web muy fácil del evento Hacker Holidays. El objetivo es encontrar
una flag expuesta en el código fuente del sitio. La app tiene el directorio
`.git/` accesible públicamente, lo que permite dumpear todo el historial del
repositorio y recuperar archivos borrados o información sensible.

## Conceptos clave

### Git directory exposure

Cuando un servidor web expone el directorio `.git/`, cualquiera puede
recuperar el historial completo del repositorio: commits, archivos borrados,
credenciales, flags hardcodeadas.

Una app correctamente desplegada nunca debería tener `.git/` en la raíz del
documento web.

### Directory enumeration

Es el proceso de descubrir rutas y archivos ocultos en un servidor web. Se
puede hacer con herramientas como `gobuster`, `feroxbuster`, `dirb` o manualmente.

### Rutas comunes a probar

| Ruta | Descripción |
|---|---|
| `/.git/` | Historial del repo |
| `/.env` | Variables de entorno |
| `/backup.zip` | Backup del código |
| `/source.zip` | Código fuente |
| `/app.py` | Archivo principal |
| `/config.py` | Configuración |
| `/robots.txt` | Directivos para crawlers |
| `/sitemap.xml` | Mapa del sitio |

## Pasos de la room

### 1. Reconocimiento inicial

Navegar a:

```http
http://MACHINE_IP:8080/
```

La página parece ser el sitio del resort Byte Lotus.

### 2. Directory enumeration con gobuster

```bash
gobuster dir -u http://MACHINE_IP:8080 \
  -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt
```

### 3. Descubrir `/.git/` expuesto

La enumeración revela que el directorio `/.git/` es accesible y listable.

```http
http://MACHINE_IP:8080/.git/
```

Contenido típico:

```text
COMMIT_EDITMSG
HEAD
branches/
config
description
hooks/
index
info/
logs/
objects/
refs/
```

### 4. Dumpear el repositorio

Con `git-dumper`:

```bash
pip install --user git-dumper
git-dumper http://MACHINE_IP:8080/.git/ ./room404_repo
```

Alternativas:

```bash
# git clone directo
git clone http://MACHINE_IP:8080/.git/ room404_repo

# wget recursivo
wget -r -np -nH --cut-dirs=1 http://MACHINE_IP:8080/.git/
```

### 5. Revisar el historial

```bash
cd room404_repo
git log --oneline
git show HEAD
git log -p
```

La flag suele estar en:

- Un archivo actual del repo.
- Un commit anterior.
- Un archivo `.env` o similar.
- Un diff entre commits.

### 6. Buscar la flag

```bash
grep -r "THM{" .
git log --all --full-history --grep="flag"
git log --all --full-history -- .env
```

## Errores comunes y lecciones

### Error: no dumpar el repo completo

Si solo descargás el `HEAD` actual, podés perder commits anteriores donde
esté la flag. Usá `git-dumper` o `git clone` para obtener todo el historial.

### Error: no revisar `.git/logs/` o reflog

A veces hay información útil en `logs/HEAD` o `logs/refs/heads/master`.

### Error: no prevenir en producción

Nunca dejar `.git/` en el document root de producción. Siempre usar
`.gitignore` y desplegar solo los archivos necesarios.

## Variantes y uso real

- **.svn/, .hg/, .bzr/ exposure:** lo mismo aplica a otros VCS.
- **.env, config.php, web.config expuestos:** archivos de configuración
  publicados por error.
- **Backup files:** `index.php.bak`, `backup.sql`, `dump.tar.gz`.

## Mitigaciones

1. No exponer `.git/` en el document root.
2. Usar despliegues limpios (solo `dist/` o archivos compilados).
3. Configurar el servidor web para negar acceso a directorios ocultos.
4. Auditar con gobuster antes de poner en producción.

## Herramientas usadas

- `gobuster` para directory enumeration.
- `git-dumper` para extraer el repo expuesto.
- `git log`, `git show`, `grep` para buscar la flag.

## Material de referencia

- OWASP Testing Guide — Information Gathering.
- TryHackMe Hacker Holidays 2026.
- GitTools (git-dumper) en GitHub.

## Autoevaluación

1. ¿Por qué es peligroso exponer `.git/` en un servidor web?
2. Nombra tres herramientas de directory enumeration.
3. ¿Qué comandos de git usás para revisar el historial de un repo dumpeado?
4. ¿Cómo evitás que `.git/` quede expuesto en producción?
