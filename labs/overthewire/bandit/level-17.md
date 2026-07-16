# OverTheWire - Bandit: Nivel 17 → 18 - Comparar archivos con `diff`

## Comando(s)

```bash
ls
```
```bash
diff passwords.new passwords.old
```

## Concepto

`diff` compara dos archivos línea por línea y muestra las diferencias. El formato `42c42` indica que la línea 42 cambió entre los archivos. La línea con `<` pertenece al primer archivo (`passwords.new`), la del `>` al segundo (`passwords.old`). El password válido es el del archivo nuevo.

## Aplicación real

- Detección de cambios en configuraciones de sistemas.
- Análisis forense comparando archivos antes y después de un incidente.
- Revisión de logs o listas de credenciales comprometidas.

## Errores comunes

- No saber cuál archivo es la versión válida (el nuevo o el viejo).
- Confundir el orden de los argumentos.
- No entender el formato `42c42`.

## Variantes útiles

- `diff -u passwords.new passwords.old` muestra diferencias en formato unificado.
- `diff -y passwords.new passwords.old` muestra ambos archivos lado a lado.
- `cmp archivo1 archivo2` compara byte a byte.
- `diff <(comando1) <(comando2)` compara salidas de comandos sin archivos temporales.
