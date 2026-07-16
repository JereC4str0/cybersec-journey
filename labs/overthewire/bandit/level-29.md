# OverTheWire - Bandit: Nivel 29 → 30 - Git branches

## Comando(s)

Desde la máquina local:
```bash
ssh bandit29@bandit.labs.overthewire.org -p 2220

cd /tmp
mkdir bandit29
cd bandit29
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo
cd repo
```

Dentro del repo:
```bash
ls
cat README.md
git branch -a
git checkout remotes/origin/dev
ls
cat README.md
```

## Concepto

La rama `master` suele contener datos de producción sanitizados. Las ramas de desarrollo (`dev`, `sploits-dev`, etc.) pueden contener credenciales reales que no se deben publicar en producción. Revisar todas las ramas, incluyendo las remotas, es clave para encontrar fugas de información.

## Aplicación real

- **Credential leaks en ramas de desarrollo**: equipos dejan passwords, API keys o tokens en `dev` o `staging`.
- **Revisión de ramas remotas**: `git branch -a` y `git branch -r` muestran ramas que no están en `master`.
- **Herramientas**: `git log --all --graph`, `git branch -a`, `truffleHog`, `gitleaks`.

## Errores comunes

- Revisar solo `master` y no las ramas remotas.
- No usar `git branch -a` para ver ramas remotas.
- No entender el estado `detached HEAD` al hacer checkout de una rama remota directamente.
- Clonar desde `localhost` dentro del servidor (OverTheWire lo bloquea).

## Variantes útiles

- `git checkout -b dev origin/dev` crea una rama local `dev` y la vincula a la remota.
- `git branch -r` lista solo las ramas remotas.
- `git log --all --graph --oneline` muestra el historial de todas las ramas.
- `git log --all --grep='password'` busca commits por mensaje en todas las ramas.
- `truffleHog git file://.` escanea secrets en el historial de todas las ramas.
