# OverTheWire - Bandit: Nivel 04 → 05 - Identificar archivos legibles con `file`

## Comando(s)

```bash
cd inhere
```
```bash
ls
```
```bash
file ./*
```
```bash
cat ./-file07
```

## Concepto

`file` identifica el tipo de contenido por magic bytes sin leerlo con cat.

## Aplicación real

Análisis de archivos sospechosos, dumps, malware y datos binarios para elegir la herramienta correcta.

## Errores comunes

- Hacer `cat` a archivos binarios y llenar la terminal de basura.
- No usar `./` para archivos que empiezan con `-`.

## Variantes útiles

- `file archivo` detecta tipo por contenido.
- `file -k` muestra más detalles.
