# OverTheWire - Bandit: Nivel 06 → 07 - Búsqueda en todo el sistema con `find`

## Comando(s)

```bash
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null
```
```bash
cat /var/lib/dpkg/info/bandit7.password
```

## Concepto

Buscar archivos en todo el sistema filtrando por propietario, grupo y tamaño.

## Aplicación real

Hunting de archivos propiedad de usuarios específicos, credenciales duras, archivos de configuración sensibles.

## Errores comunes

- Errores de tipeo en flags (`-grpup`).
- No redirigir stderr (`2>/dev/null`) y llenar pantalla de permiso denegado.

## Variantes útiles

- `find / -user root -perm -4000` archivos SUID de root.
- `find / -type f -name '*.bak'` backups.
