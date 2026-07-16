# Resumen: OverTheWire - Bandit Niveles 27 → 33

## Serie: Git, hooks y escape de shell restringido

Esta serie de niveles cubre fugas de credenciales en repositorios Git y el escape de shells restringidos. La idea general es pasar de encontrar datos expuestos a entender cómo los controles del lado del cliente pueden ser bypassados y cómo los hooks del servidor pueden ejecutar lógica sensible.

---

## Niveles y técnicas

| Nivel | Tema | Comandos clave | Concepto central |
|-------|------|----------------|------------------|
| 27 → 28 | Git clone | `git clone ssh://...` | El password está en un archivo del repo. Hay que clonar desde la máquina local porque OverTheWire bloquea SSH desde localhost. |
| 28 → 29 | Git history | `git log`, `git show <hash>` | La credencial fue borrada del archivo actual pero queda en el historial de commits. |
| 29 → 30 | Git branches | `git branch -a`, `git checkout remotes/origin/dev` | Las ramas de desarrollo pueden contener datos que `master` de producción no tiene. |
| 30 → 31 | Git tags | `git tag`, `git show <tag>` | Los tags marcan versiones y pueden contener objetos anotados con datos adicionales. |
| 31 → 32 | Git hooks + `.gitignore` | `echo "..." > key.txt`, `git add -f`, `git push` | `.gitignore` es un control del cliente. El servidor puede validar el push con un hook y devolver información. |
| 32 → 33 | Escape de shell restringido | `$0`, `whoami`, `cat /etc/bandit_pass/bandit33` | Un wrapper que transforma comandos puede ser bypassado invocando la shell real a través de `$0`. |

---

## Lecciones principales

1. **`.gitignore` no es seguridad**: solo guía al cliente. Cualquiera con acceso al repo puede hacer `git add -f` y subir archivos ignorados.
2. **El historial de Git conserva todo**: commits borrados, ramas antiguas y tags pueden contener secrets.
3. **Las ramas y tags son parte del alcance**: `master` no es el último lugar donde buscar.
4. **Los hooks del servidor ejecutan código**: `pre-receive`, `post-receive` y `update` pueden validar, filtrar o responder al contenido del push.
5. **Los shells restringidos no son infalibles**: wrappers simples como convertir a mayúsculas se bypassan con variables del entorno como `$0`.

---

## Aplicación ofensiva

- **Credential leaks**: buscar secrets en historial, ramas y tags de repos públicos o internos.
- **Bypass de controles**: usar `git add -f` para subir archivos que el equipo cree protegidos por `.gitignore`.
- **Ataques a hooks**: aprovechar hooks del servidor que ejecutan comandos con datos del push (command injection, RCE).
- **Escape de jaulas**: escapar de `rbash`, shells restringidos o contenedores mediante variables de entorno o binarios que permiten lanzar shells.

---

## Defensa recomendada

- No depender de `.gitignore` para proteger datos sensibles.
- Usar hooks `pre-receive` para bloquear secrets, archivos por nombre/extensión y pushes directos a `master`.
- Escanear historial con `truffleHog`, `gitleaks` o `git-secrets`.
- Usar branch protection y requerir revisiones de PR.
- No ejecutar hooks del servidor con privilegios elevados ni usar `eval` con contenido de push.
- Para shells restringidos, usar `rbash` bien configurado, chroot con privaciones o soluciones de contenedor con namespaces.

---

## Errores comunes

- Clonar desde `localhost` dentro del servidor de OverTheWire (está bloqueado).
- Revisar solo el archivo actual y no el historial, ramas o tags.
- No usar `git add -f` cuando el archivo está en `.gitignore`.
- Pensar que un push rechazado significa que el hook no ejecutó nada.
- Intentar comandos directamente en el shell restringido sin probar `$0`.

---

## Variantes útiles

- `git log --all --oneline` y `git log --all --graph`.
- `git branch -a` y `git branch -r`.
- `git show <hash>:<archivo>` para ver un archivo en un punto específico.
- `git ls-remote --tags` para listar tags sin clonar.
- `git check-ignore -v <archivo>` para entender por qué un archivo es ignorado.
- `git add -f` o `git add --force` para trackear archivos ignorados.
- `$0`, `$SHELL`, `bash -i`, `python3 -c 'import pty; pty.spawn("/bin/bash")'` para escapes de shells restringidos.

---

## Nota sobre documentación

Las contraseñas individuales no se incluyen en este resumen ni en los writeups por nivel. Se guardan por fuera del repo para mantener el repositorio público limpio.
