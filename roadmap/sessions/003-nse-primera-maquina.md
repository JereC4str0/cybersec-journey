# Sesión 003 — NSE + primera máquina vulnerable (Kioptrix L1)

> Modo profesor: cada ejercicio viene con su material de estudio exacto.
> Parte A cierra el Bloque 02 (Networking). Parte B arranca Bloque 05
> (metodología) con la primera máquina real del portfolio.

## Situación actual

- Bloque 02: faltaba solo el ejemplo de NSE para cerrar la exit gate.
- Entorno verificado: VirtualBox instalado, 17 GB libres, ~3.8 GB RAM.
- Lab local (sin VPN): VM vulnerable propia, descargada de VulnHub.

## Objetivo de la sesión

1. Cerrar Bloque 02 con el ejemplo de NSE documentado.
2. Levantar el primer lab de máquina vulnerable en VirtualBox.
3. Aplicar la metodología completa de enum recon → scanning → enumeration
   contra un objetivo real (sin exploit todavía: eso es sesión 004).

---

## Parte A — NSE (cierra Bloque 02)

### Material de estudio (exacto)

1. **Nmap NSE docs (oficial)**: https://nmap.org/book/nse.html
   - Solo la sección "Usage and Examples" + la categoría `default`.
2. **Nmap Reference Guide**: https://nmap.org/book/man.html
   - Buscar `-sC` y `--script` en la página.

### Ejercicio

1. Correr NSE por defecto contra tu propio SSH:

```bash
nmap -sV -sC -p 22 localhost
```

2. Correr un script específico de enumeración:

```bash
nmap --script ssh2-enum-algos -p 22 localhost
```

3. Responder en la nota:
   - ¿Qué hace `-sC` exactamente? (qué categoría de scripts corre)
   - Nombrar 2 hallazgos concretos del output y explicar por qué le
     importan a un pentester.
   - ¿Qué diferencia hay entre `-sC` y `--script nombre`?

### Entregable

- `notes/02-networking/04-nse-basico.md` (formato repaso, outputs propios).

Con eso la exit gate del Bloque 02 queda completa y se marca en
`roadmap/progress.md`.

---

## Parte B — Lab: Kioptrix Level 1

Por qué esta máquina: es LA primera VM clásica de pentesting (la usa
TCM Security en su curso gratuito), pesa poco (~1 GB), corre con 512 MB
de RAM y tiene vulnerabilidades reales y documentadas.

### Material de estudio (exacto)

1. **TCM Security — Practical Ethical Hacking (curso completo gratis en
   YouTube)**: https://www.youtube.com/watch?v=3Kq1MIfTWCE
   - Sección "Scanning & Enumeration" (mirar ANTES de escanear la VM).
   - Sección "Exploitation Basics" se mira recién en la sesión 004.
2. **HackTricks — Pentesting Methodology**:
   https://book.hacktricks.wiki/en/generic-methodologies-and-resources/pentesting-methodology.html
   - Solo el diagrama de fases: recon → enum → exploitation → post.

### Ejercicio

1. **Descargar la VM** (VulnHub, espejo oficial):

```bash
mkdir -p ~/vms/kioptrix-l1 && cd ~/vms/kioptrix-l1
curl -LO https://download.vulnhub.com/kioptrix/Kioptrix_Level_1.rar
```

2. **Extraer e importar** en VirtualBox:
   - Extraer el .rar (hay un .vmdk adentro).
   - Crear VM nueva: Linux / Other Linux, 512 MB RAM, disco existente
     (el .vmdk extraído).
   - Red: **Host-only Adapter** (vboxnet0). Nada de NAT con salida a
     internet para la VM vulnerable.

3. **Encontrar la IP de la VM** sin mirar su consola:
   - `ip a` en el host → identificar la IP de vboxnet0 (típico 192.168.56.1).
   - Ping scan al segmento host-only:

```bash
nmap -sn 192.168.56.0/24
```

4. **Enumeración completa** contra la IP de la VM:

```bash
nmap -p- --open -sS --min-rate 2000 -v -n <IP_VM>     # fase 1: todos los puertos
nmap -sCV -p <puertos_abiertos> <IP_VM> -oN kioptrix-enum.txt
```

5. **Analizar servicios**: para CADA puerto abierto responder:
   - ¿Qué servicio y versión es?
   - ¿Es una versión vieja? (buscar la versión + "vulnerability" en Google)
   - ¿Qué intentaría un atacante contra ese servicio?

### Reglas de la casa

- Todo escaneo es contra TU VM en red host-only. Nada externo.
- Los outputs van sanitizados al repo (IPs host-only no son sensibles,
  pero el hábito se practica igual).
- **NO explotar todavía.** La enumeración es un entregable en sí misma.
  Caer en "escaneo y exploit inmediato" es el error #1 del principiante.

---

## Entregables públicos

- `notes/02-networking/04-nse-basico.md`
- `labs/kioptrix/level-1-enumeracion.md` — análisis de la enum (sin exploit)
- `labs/tracking.md` — agregar fila de Kioptrix L1 con estado "enumerando"
- Commit chico por cada entregable.

## Desafío extra

- Comparar el output de `-sC` contra la VM vs el de tu propia máquina:
  ¿qué scripts dispararon en cada caso y por qué?

## Criterio de cierre de sesión

- Exit gate de Bloque 02 marcada honestamente en `progress.md`.
- VM corriendo, IP encontrada por escaneo propio, enum completo
  documentado con análisis por servicio.
- Próxima sesión (004): explotación guiada de Kioptrix L1 con material
  específico según los servicios encontrados.
