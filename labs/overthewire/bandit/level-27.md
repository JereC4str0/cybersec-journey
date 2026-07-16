# OverTheWire - Bandit: Nivel 27 → 28 - Git clone

## Comando(s)

Desde la máquina local:
```bash
cd /tmp
mkdir bandit27
cd bandit27
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
```

Dentro del repo:
```bash
cd repo
ls
cat README
```

## Concepto

El password está almacenado en un repositorio Git. OverTheWire bloquea conexiones SSH desde `localhost` dentro del servidor, por lo que hay que clonar desde la máquina local. El password se encontraba en el archivo `README` del repositorio.

## Aplicación real

- **Credential leaks**: desarrolladores suben secrets, passwords o API keys a repositorios Git.
- **Revisión de historial**: a veces las credenciales se borran del archivo actual pero quedan en commits anteriores.
- **Herramientas**: `git log`, `git show`, `git grep`, `truffleHog`, `gitleaks`.

## Errores comunes

- Intentar clonar desde `localhost` dentro del servidor (OverTheWire lo bloquea).
- No verificar el historial de commits.
- Usar el usuario equivocado en la URL SSH.

## Variantes útiles

- `git log --all --oneline` muestra todos los commits.
- `git show <hash>` muestra el contenido de un commit.
- `git branch -a` lista ramas locales y remotas.
- `git log -p README` muestra todos los cambios de un archivo.
- `git log --all --grep='password'` busca commits por mensaje.
- `truffleHog` o `gitleaks` escanean secrets en repositorios.
