# OverTheWire - Bandit: Nivel 26 → 27 - Setuid de bandit27

## Comando(s)

```bash
ls
```
```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

## Concepto

`bandit27-do` es un binario setuid propiedad de `bandit27`. Cuando `bandit26` lo ejecuta, el binario corre con los permisos de `bandit27`, permitiendo leer `/etc/bandit_pass/bandit27`.

## Aplicación real

- **Privilege escalation**: binarios setuid son un vector clásico para escalar privilegios en Linux.
- **Auditoría**: `find / -perm -4000` lista estos binarios.
- **GTFOBins**: repositorio de técnicas para explotar binarios setuid conocidos.

## Errores comunes

- Olvidar `./` antes del nombre del binario.
- No verificar que el binario es setuid con `ls -la`.
- Intentar leer el archivo protegido directamente sin usar el binario.

## Variantes útiles

- `find / -perm -4000 -type f 2>/dev/null` encuentra setuid binaries.
- `find / -perm -u=s 2>/dev/null` alternativa.
- https://gtfobins.github.io/ para técnicas de explotación.
- `stat -c '%a %U %G %n' ./bandit27-do` muestra permisos y propietario.
