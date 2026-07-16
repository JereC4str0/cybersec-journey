# OverTheWire - Bandit: Nivel 19 → 20 - Binarios setuid

## Comando(s)

```bash
ls -la
```
```bash
file bandit20-do
```
```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

## Concepto

`bandit20-do` es un binario ELF con el bit **setuid** activado. El bit setuid permite que un ejecutable se corra con los privilegios de su propietario, no del usuario que lo ejecuta. Como el propietario es `bandit20`, cualquier comando lanzado por este binario corre con permisos de `bandit20`.

## Aplicación real

- **Privilege escalation**: binarios setuid propiedad de root o de usuarios con más privilegios son uno de los primeros vectores a revisar en Linux.
- **Persistencia**: un atacante puede dejar un binario setuid como backdoor.
- **Auditoría**: encontrar setuid binaries inesperados con `find / -perm -4000 2>/dev/null`.

## Errores comunes

- No verificar permisos y tratar el binario como un ejecutable común.
- No buscar binarios setuid durante la fase de post-explotación.
- Intentar leer el archivo protegido directamente sin usar el binario.

## Variantes útiles

- `find / -perm -4000 2>/dev/null` lista todos los setuid binaries.
- `find / -perm -2000 2>/dev/null` lista setgid binaries.
- `getcap -r / 2>/dev/null` busca capabilities.
- https://gtfobins.github.io/ tiene técnicas de explotación para binarios conocidos.
