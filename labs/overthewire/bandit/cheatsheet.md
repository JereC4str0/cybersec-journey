# Cheatsheet - Bandit

## Navegación y lectura

| Comando | Uso | Ejemplo |
|---------|-----|---------|
| `ssh -p 2220 user@host` | Conectar por SSH en puerto no estándar | `ssh bandit0@bandit.labs.overthewire.org -p 2220` |
| `ls -la` | Listar archivos incluyendo ocultos | `ls -la inhere/` |
| `cat archivo` | Mostrar contenido de archivo | `cat readme` |
| `cd directorio` | Cambiar de directorio | `cd /tmp/work` |

## Búsqueda y filtrado

| Comando | Uso | Ejemplo |
|---------|-----|---------|
| `grep patrón archivo` | Buscar patrón en archivo | `grep 'millionth' data.txt` |
| `find . -type f -size 1033c` | Buscar por tamaño | `find . -type f -size 1033c ! -executable` |
| `find / -user X -group Y` | Buscar por propietario/grupo | `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null` |
| `sort archivo | uniq -u` | Líneas únicas | `sort data.txt | uniq -u` |

## Binarios y codificación

| Comando | Uso | Ejemplo |
|---------|-----|---------|
| `file archivo` | Identificar tipo de archivo | `file ./*` |
| `strings archivo` | Extraer texto legible | `strings data.txt | grep '='` |
| `base64 -d archivo` | Decodificar base64 | `base64 -d data.txt` |
| `xxd -r archivo` | Revertir hexdump | `xxd -r data.txt > binario` |
| `tr 'A-Za-z' 'N-ZA-Mn-za-m'` | ROT13 | `cat data.txt | tr ...` |

## Compresión y archivos

| Comando | Uso | Ejemplo |
|---------|-----|---------|
| `gunzip archivo.gz` | Descomprimir gzip | `gunzip archivo.gz` |
| `bunzip2 archivo.bz2` | Descomprimir bzip2 | `bunzip2 archivo.bz2` |
| `tar xvf archivo` | Extraer tar | `tar xvf archivo.tar` |
| `tar tvf archivo` | Listar contenido sin extraer | `tar tvf archivo.tar` |

## Red

| Comando | Uso | Ejemplo |
|---------|-----|---------|
| `nc host puerto` | Conexión TCP simple | `nc localhost 30000` |
| `openssl s_client -connect host:port` | Cliente SSL/TLS | `openssl s_client -connect localhost:30001 -ign_eof` |
| `nmap -p rango -sV host` | Escanear puertos | `nmap -p 31000-32000 -sV localhost` |

## SSH y claves

| Comando | Uso | Ejemplo |
|---------|-----|---------|
| `ssh -i key user@host` | SSH con clave privada | `ssh -i ~/key bandit14@host` |
| `scp -P 2220 user@host:ruta destino` | Copiar archivo por SSH | `scp -P 2220 ...` |
| `chmod 600 key` | Permisos estrictos para clave | `chmod 600 ~/key` |

## Trucos comunes

- Archivos con `-` al inicio: `cat ./-` o `cat -- -`.
- Archivos con espacios: `cat "archivo con espacios"` o `cat 'archivo con espacios'`.
- Archivos ocultos: `ls -la`.
- Redirigir errores: `2>/dev/null`.
- Pipe de entrada: `cat archivo | comando`.
