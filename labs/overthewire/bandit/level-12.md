# OverTheWire - Bandit: Nivel 12 → 13 - Hexdump, gzip, bzip2, tar anidados

## Comando(s)

```bash
xxd -r ~/data.txt > archivo
```
```bash
file archivo
```
```bash
mv archivo archivo.gz && gunzip archivo.gz
```
```bash
mv archivo archivo.bz2 && bunzip2 archivo.bz2
```
```bash
tar xvf archivo
```
```bash
file <nuevo_archivo>
```

## Concepto

Cadena de ofuscación: hexdump → compresión gzip/bzip2 → empaquetado tar. Se identifica con `file` y se descompone capa por capa.

## Aplicación real

Análisis de malware, steganografía y exfiltración de datos ofuscados.

## Errores comunes

- No usar `file` antes de intentar descomprimir.
- No dar extensión correcta antes de `gunzip`/`bunzip2`.

## Variantes útiles

- `xxd archivo` para hacer hexdump.
- `tar tvf archivo` lista contenido sin extraer.
- `gzip -l archivo.gz` muestra información sin descomprimir.
