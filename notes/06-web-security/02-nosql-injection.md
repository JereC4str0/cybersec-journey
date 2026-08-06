# NoSQL Injection — Fundamentos

> Nota de repaso. Bloque 04 — Web security.
> Fuente: TryHackMe NoSQL Injection room, MongoDB docs, PortSwigger NoSQL topic.

## Concepto

NoSQL Injection es una familia de ataques donde el input del usuario modifica
una query en una base de datos no relacional (MongoDB, CouchDB, Redis, etc.).

La causa raíz es la misma que en SQL injection: **el input se concatena o
mezcla con la query sin separar datos de código.**

## Diferencia clave con SQL injection

| SQL | MongoDB |
|---|---|
| Queries en texto plano. | Queries en JSON-like / arrays asociativos. |
| Rompés comillas para salir. | Inyectás operadores u objetos dentro del filtro. |
| `OR 1=1` | `{'$ne': null}` |
| `UNION SELECT` | No existe; exfiltrás con regex o JavaScript. |

## Documentos y colecciones

En MongoDB:
- **Documento:** un objeto JSON-like con campos arbitrarios.
- **Colección:** grupo de documentos (equivalente a tabla en SQL).
- **Base de datos:** grupo de colecciones.

Ejemplo de documento:

```json
{
  "_id": ObjectId("..."),
  "username": "lphillips",
  "first_name": "Logan",
  "age": 65,
  "email": "lphillips@example.com"
}
```

## Query básica en MongoDB

```javascript
// Equivalente a SELECT * FROM people WHERE last_name = 'Sandler'
db.people.find({ "last_name": "Sandler" })

// AND implícito
db.people.find({ "gender": "male", "last_name": "Phillips" })

// Operador $lt (menor que)
db.people.find({ "age": { "$lt": 50 } })
```

## Tipos de NoSQL injection

### Operator Injection

El atacante envía un array u objeto que el backend usa como valor de un campo,
cambiando el comportamiento del filtro.

**Ejemplo clásico — authentication bypass:**

Query vulnerable en PHP:

```php
$q = new MongoDB\Driver\Query([
  'username' => $user,
  'password' => $pass
]);
```

Si enviamos por POST:

```http
user[$ne]=xxxx&pass[$ne]=yyyy
```

PHP convierte esto en:

```php
$user = ['$ne' => 'xxxx'];
$pass = ['$ne' => 'yyyy'];
```

La query final:

```javascript
{ "username": { "$ne": "xxxx" }, "password": { "$ne": "yyyy" } }
```

Esto devuelve cualquier usuario cuyo username no sea `xxxx` y password no sea
`yyyy` — es decir, todos.

### Syntax Injection

Ocurre cuando el desarrollador usa queries en JavaScript en lugar de los
filtros nativos de MongoDB, típicamente con `$where`.

```javascript
db.users.find({ "$where": "this.username == '" + username + "'" });
```

Si `username` es `admin' || 1 || 'x`, la query se convierte en:

```javascript
this.username == 'admin' || 1 || 'x'
```

Siempre verdadero, devuelve todos los documentos.

## Operadores útiles para inyección

| Operador | Significado | Uso ofensivo |
|---|---|---|
| `$ne` | Not equal | `{ "password": { "$ne": "" } }` |
| `$nin` | Not in array | Excluir usuarios conocidos para pivotear a otros. |
| `$gt` / `$lt` | Greater / less than | Comparar caracteres. |
| `$regex` | Expresión regular | Extraer passwords carácter por carácter. |
| `$where` | Ejecutar JavaScript | Syntax injection. |
| `$exists` | Campo existe | `{ "password": { "$exists": true } }` |

## Exfiltración con `$regex`

MongoDB permite regex en queries. Esto permite ataques tipo blind/hangman:

```javascript
{ "username": "admin", "password": { "$regex": "^a" } }
```

Si el login es exitoso, el password empieza con `a`. Si no, probamos `b`, `c`,
etc. Luego el segundo carácter, y así sucesivamente.

Esto es equivalente a Blind SQLi pero usando regex en lugar de `SUBSTRING()`.

## Mitigaciones

1. **Parameterized queries / input sanitization:** usar librerías que
   serialicen correctamente los inputs.
2. **No usar `$where` con concatenación:** evitar JavaScript en queries.
3. **Validar tipos:** si esperás un string, rechazá arrays u objetos.
4. **Principio de mínimo privilegio:** la app no debería tener permisos de
   administración en la DB.
5. **WAF** como capa adicional, nunca como única defensa.

## Detección

Probar en cualquier input:

```http
user[$ne]=test&pass[$ne]=test
username[$regex]=.*
username[$exists]=true
```

Si la app acepta el array y cambia el comportamiento, hay inyección.

## Autoevaluación

1. ¿Cuál es la diferencia entre Operator Injection y Syntax Injection en
   MongoDB?
2. ¿Cómo envía PHP un array a través de un POST request?
3. ¿Por qué `$where` es especialmente peligroso?
4. ¿Qué operador permite extraer passwords carácter por carácter?
5. ¿Por qué un WAF que solo filtra comillas simples no protege contra NoSQLi?
