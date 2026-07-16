# OverTheWire - Bandit: Nivel 31 → 32 - Git push + hooks

## Comando(s)

Desde la máquina local:
```bash
ssh bandit31@bandit.labs.overthewire.org -p 2220

cd /tmp
mkdir bandit31
cd bandit31
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo
cd repo
```

Dentro del repo:
```bash
cat .gitignore
cat README.md
echo "May I come in?" > key.txt
git add -f key.txt
git commit -m "add key.txt"
git push origin master
```

## Concepto

`.gitignore` es una regla del lado del cliente que evita que `git add` trackee archivos por defecto, pero no impide que se suban si se usa `git add -f`. El servidor puede tener un hook `pre-receive` o `post-receive` que valide el contenido del push antes de aceptarlo o rechazarlo. En este caso, el hook ejecutó la validación, devolvió la password en el output remoto y luego rechazó el push.

## Aplicación real

- **Bypass de controles del cliente**: `.gitignore` no protege el servidor. Un atacante con acceso puede subir archivos ignorados.
- **Validación en servidor**: hooks `pre-receive`, `update` y `post-receive` permiten ejecutar lógica antes, durante o después de un push.
- **Ejecución de código**: hooks que ejecutan scripts con contenido del push pueden ser vectores de command injection o RCE si no se sanitizan.
- **Defensa**: usar hooks `pre-receive` para bloquear archivos por nombre, extensión o contenido; branch protection; scanning de secrets en servidor.

## Errores comunes

- Intentar `git add key.txt` sin `-f` y que Git lo ignore por `.gitignore`.
- No usar el contenido exacto que pide el reto (`May I come in?`).
- Confundirse porque el push fue rechazado: el hook pudo ejecutar la validación antes del rechazo.
- Depender de `.gitignore` como única barrera de seguridad.

## Variantes útiles

- `git check-ignore -v key.txt` explica por qué un archivo está ignorado.
- `git add --force key.txt` equivale a `git add -f key.txt`.
- `git ls-files` verifica qué archivos están trackeados.
- `git push --no-verify` salta hooks `pre-commit`/`pre-push` locales, pero no los del servidor.
- `git config core.excludesFile` define un archivo global de exclusión.
- `truffleHog` o `gitleaks` detectan secrets subidos al historial.
