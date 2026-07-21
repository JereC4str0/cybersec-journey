# Port Scanner — scaffold de aprendizaje

> Objetivo: aprender Python desde 0 modificando una herramienta chica, no escribiéndola desde cero.
>
> Uso ético: solo localhost, VMs propias o labs autorizados.

## Qué es esto

`portscanner.py` es un scaffold mínimo y runnable. Ya funciona. Tu trabajo no es “crear un scanner desde 0”, sino entenderlo, correrlo y modificarlo en pasos chicos.

## Cómo correrlo

Desde la raíz del repo:

```bash
python3 scripts/port-scanner/portscanner.py -h
python3 scripts/port-scanner/portscanner.py -t 127.0.0.1 -p 1-1024
```

O entrando a la carpeta:

```bash
cd scripts/port-scanner
python3 portscanner.py -t 127.0.0.1 -p 1-1024
```

## Qué mirar en el código

En `portscanner.py`, identificá estas 4 piezas:

1. `argparse` — define flags como `-t` y `-p`.
2. `parse_port_range()` — convierte texto como `1-1024` en una lista de números.
3. `scan_port()` — abre un socket TCP y usa `connect_ex`.
4. `main()` — une todo y decide qué se imprime.

## Micro-tareas guiadas

Hacé una por vez y commiteá cada cambio chico:

1. Correr el scanner sin modificar nada y guardar la salida en tus notas.
2. Cambiar el timeout de `scan_port()` de `1.0` a `0.3` y anotar qué cambia.
3. Agregar un print al final que diga cuántos puertos se revisaron.
4. Agregar una opción `--show-closed` que también muestre puertos cerrados.
5. Escribir `notes/03-scripting/01-python-scaffold.md` respondiendo:
   - ¿Qué hace `argparse`?
   - ¿Qué devuelve `connect_ex` cuando el puerto está abierto?
   - ¿Por qué usamos `with socket.socket(...)`?
   - ¿Qué riesgo tiene escanear sin autorización?

## Pista para `--show-closed`

No hace falta que lo escribas desde cero. Buscá dónde está este bloque:

```python
if scan_port(args.target, port):
    print(f"[OPEN] {port}/tcp")
```

La idea es agregar un flag booleano en `build_parser()` y luego convertir ese `if` en un `if/else`.

## Criterio de cierre

Esta parte está completa cuando:

- corriste el scanner,
- hiciste al menos 2 modificaciones chicas,
- escribiste la nota `notes/03-scripting/01-python-scaffold.md`,
- no publicaste outputs sensibles,
- dejaste commits chicos y claros.
