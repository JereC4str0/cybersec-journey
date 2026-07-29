# Writeup: TryHackMe — CSRF (V2)

## Información
- **Plataforma:** TryHackMe
- **Room:** CSRF (`/room/csrfV2`)
- **Path:** Web Application Pentesting
- **Dificultad:** Easy / Fundamentals
- **Técnicas principales:** CSRF básico, GET-based CSRF, hidden image/link, CSRF token
- **Fecha:** 2026-07-28

## Resumen ejecutivo

Room introductoria que simula un banco online (`mybank.thm:8080`) y un mailbox (`mailbox.thm:8081`) para demostrar dos escenarios de Cross-Site Request Forgery:

1. **CSRF exitoso:** el formulario de transferencia no valida origen ni token, por lo que un enlace o imagen oculta en un correo ejecuta una acción en nombre de la víctima autenticada.
2. **CSRF mitigado:** el banco agrega un `csrf_token` y el ataque ya no funciona.

## Conceptos clave

### ¿Qué es CSRF?

El atacante fuerza al navegador de una víctima autenticada a realizar una petición no deseada a un sitio en el que confía. El navegador envía las cookies automáticamente, así que el servidor procesa la acción como legítima.

**Condiciones necesarias:**
- La víctima tiene una sesión activa en el sitio vulnerable.
- La aplicación no valida el origen de la request (no CSRF token, no SameSite estricto, no verificación de `Origin`/`Referer`).
- La acción se puede realizar con una petición que el navegador pueda enviar sin interacción directa (GET, POST auto-submit, etc.).

### Hidden image / hidden link

Técnica para enviar una request GET sin que el usuario lo note:

```html
<img src="http://mybank.thm:8080/transfer.php?to_account=GB82MYBANK5698&amount=1000" width="0" height="0">
```

El navegador carga el `src` de la imagen automáticamente, enviando las cookies de `mybank.thm` si la víctima está autenticada.

**No requiere que `src` sea una imagen real.** El navegador hace la request igual; puede devolver un error, un pixel transparente o cualquier respuesta.

### CSRF token

El servidor incluye un valor aleatorio en el formulario y lo verifica al recibir la petición. Si el atacante no conoce el token, no puede armar un payload válido.

```html
<input type="hidden" name="csrf_token" value="aleatorio">
```

## Ataque #1: transferencia sin protección

### Flujo

1. El atacante inicia sesión en el banco con sus credenciales y descubre que `transfer.php` acepta una transferencia vía GET sin token.
2. El atacante envía un correo a Josh con un enlace (o imagen) que apunta a la URL de transferencia.
3. Josh, autenticado en el banco desde su navegador, abre el correo y hace clic.
4. El navegador envía la request con las cookies de sesión; el banco procesa la transferencia.

### URL maliciosa de ejemplo (sintética, sin valores reales)

```
http://mybank.thm:8080/dashboard.php?to_account=<cuenta-atacante>&amount=1000
```

### Por qué funciona

El backend no verifica:
- Si la request fue iniciada por el propio sitio.
- Si hay un token anti-CSRF.
- Si el método es seguro para una acción destructiva.

## Ataque #2: CSRF detectado (mitigado con token)

El banco agrega un `csrf_token` vinculado a la sesión:

```html
<input type="hidden" id="csrf_token" name="csrf_token" value="<?php echo $_COOKIE['csrf-token']; ?>">
```

Al hacer clic en el enlace malicioso, la request no incluye el token. El servidor rechaza la operación y detecta el intento de CSRF.

## Comandos / herramientas usadas

- Navegador dentro de la VM de la room (Chrome con la sesión de Josh).
- `http://mailbox.thm:8081` — bandeja de entrada de la víctima.
- `http://mybank.thm:8080` — aplicación vulnerable del banco.
- DevTools del navegador (pestaña Network y Application → Cookies) para observar cookies y requests.

## Errores comunes y lecciones

### Error: intentar ejecutar el ataque desde el navegador local

**Síntoma:** `isBanned cookie not found in request` al hacer clic en el enlace del correo.

**Causa:** CSRF requiere que la víctima tenga una sesión activa en el sitio vulnerable. Desde el navegador local no se tiene la sesión de Josh en la VM de la room.

**Solución:** ejecutar el ataque desde el navegador de la VM proporcionada por TryHackMe, donde Josh mantiene su sesión iniciada.

### Error: confundir `target` con `src`

- `<a href="..." target="_blank">` abre en una nueva pestaña cuando el usuario hace clic.
- `<img src="...">` hace una request automática al cargar la página; no requiere clic ni `target`.

### Error: pensar que `src` debe apuntar a una imagen real

La URL del `src` puede ser cualquier endpoint; el navegador hace la request igual. Esto es lo que permite abusar de `<img>` para enviar requests GET a endpoints state-changing.

## Variantes y uso real

- **Auto-submitting form:** formulario HTML oculto con JavaScript que hace `submit()` automático para enviar POST en lugar de GET.
- **Fetch/XHR cross-site:** modernamente limitado por CORS, pero puede servir si el backend no valida el contenido y las cookies son `SameSite=None`.
- **SameSite bypasses:** en entornos reales, `SameSite=Lax` aún permite ciertos ataques (navegación top-level, POST via GET en endpoints con method override, etc.).
- **JSON CSRF / content-type bypasses:** enviar requests con `Content-Type: text/plain` para evitar preflight CORS en endpoints legacy.

## Mitigaciones

- **CSRF tokens:** valor aleatorio vinculado a la sesión, validado en cada acción state-changing.
- **SameSite cookies:** `SameSite=Lax` mitiga la mayoría de CSRF via POST; `SameSite=Strict` es más fuerte pero rompe flujos de deep-linking.
- **Verificación de origen:** revisar headers `Origin` y `Referer` en peticiones sensibles.
- **Métodos HTTP correctos:** las acciones destructivas deben ser POST/PUT/PATCH/DELETE, nunca GET.
- **Re-autenticación:** para acciones críticas (transferencia, cambio de contraseña, cambio de email), pedir contraseña o 2FA.

## Autoevaluación

1. ¿Por qué el ataque de imagen de 1 píxel no requiere que el usuario haga clic?
2. ¿Qué tres condiciones deben cumplirse para que un ataque CSRF sea exitoso?
3. ¿Por qué una cookie `SameSite=Strict` bloquea este tipo de CSRF via `<img>`?
4. ¿Cuál es la diferencia entre el vector `<a href>` y `<img src>` desde el punto de vista del navegador?
5. ¿Por qué el segundo ataque de la room falla después de que el banco agrega `csrf_token`?
6. ¿Qué método HTTP es incorrecto para una acción de transferencia de fondos y por qué?

---

**Reglas del repo:** este writeup no incluye flags ni respuestas literales de la room.
