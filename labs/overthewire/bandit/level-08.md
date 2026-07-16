# OverTheWire - Bandit: Nivel 08 → 09 - Encontrar líneas únicas con `sort | uniq`

## Comando(s)

```bash
sort data.txt | uniq -u
```

## Concepto

`sort` ordena líneas; `uniq -u` muestra las que aparecen exactamente una vez.

## Aplicación real

Análisis de logs para detectar anomalías, eventos únicos o duplicados.

## Errores comunes

- Usar `uniq` sin `sort` antes (solo detecta duplicados consecutivos).
- Confundir `uniq -u` con `uniq -d` (este último muestra duplicados).

## Variantes útiles

- `sort | uniq -c` cuenta ocurrencias.
- `sort | uniq -d` muestra duplicados.
