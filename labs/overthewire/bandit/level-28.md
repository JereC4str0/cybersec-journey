# OverTheWire - Bandit: Nivel 28 → 29 - Git history

## Comando(s)

Desde la máquina local:
```bash
ssh bandit28@bandit.labs.overthewire.org -p 2220

cd /tmp
mkdir bandit28
cd bandit28
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
cd repo
```

Dentro del repo:
```bash
ls
cat README.md
git log
git branch -a
git log --all --oneline
git show <hash>
```

## Concepto

El archivo `README.md` actual tiene la password censurada. La password real fue subida en un commit anterior y luego "corregida" en el commit `fix info leak`. El historial de Git conserva todos los cambios, por lo que se puede recuperar la credencial original revisando commits anteriores.

## Aplicación real

- **Credential leaks**: developers commitean secrets y luego los borran, pero quedan en el historial.
- **Revisión de historial**: a veces las credenciales se borran del archivo actual pero quedan en commits anteriores.
- **Herramientas**: `git log`, `git show`, `git grep`, `truffleHog`, `gitleaks`.

## Errores comunes

- Revisar solo el archivo actual y no el historial.
- No listar ramas remotas (`git branch -a`).
- Clonar desde `localhost` dentro del servidor (OverTheWire lo bloquea).

## Variantes útiles

- `git log -p README.md` muestra todos los cambios del archivo.
- `git log --all --grep='password'` busca commits por mensaje.
- `git show <hash>:README.md` muestra el contenido de un archivo en un commit específico.
- `git branch -a` lista ramas locales y remotas.
- `truffleHog` o `gitleaks` escanean secrets en repositorios.
