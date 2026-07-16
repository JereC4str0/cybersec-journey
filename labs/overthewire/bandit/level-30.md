# OverTheWire - Bandit: Nivel 30 → 31 - Git tags

## Comando(s)

Desde la máquina local:
```bash
ssh bandit30@bandit.labs.overthewire.org -p 2220

cd /tmp
mkdir bandit30
cd bandit30
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo
cd repo
```

Dentro del repo:
```bash
git tag
git show <tag>
```

## Concepto

Los tags en Git marcan puntos específicos del historial, generalmente versiones de release. A diferencia de las ramas, los tags no se mueven con nuevos commits. Pueden contener objetos anotados con metadatos adicionales, por lo que conviene revisarlos al buscar información sensible.

## Aplicación real

- **Versiones de release**: los tags como `v1.0.0` pueden apuntar a snapshots estables que contienen credenciales olvidadas.
- **Objetos anotados**: `git show <tag>` muestra el contenido del tag, que puede incluir mensajes o datos extra.
- **Herramientas**: `git tag`, `git show`, `git ls-remote --tags`, `truffleHog`, `gitleaks`.

## Errores comunes

- Revisar solo `master` y no los tags.
- No usar `git show` para inspeccionar el contenido de un tag.
- Asumir que un tag es solo un nombre sin datos adicionales.
- Clonar desde `localhost` dentro del servidor (OverTheWire lo bloquea).

## Variantes útiles

- `git ls-remote --tags` lista tags remotos sin clonar el repo.
- `git show <tag>:<archivo>` muestra el contenido de un archivo en el tag.
- `git checkout <tag>` permite revisar el estado del repo en ese tag.
- `git tag -n` muestra los mensajes de tags anotados.
- `truffleHog git file://.` escanea secrets en el historial, tags incluidos.
