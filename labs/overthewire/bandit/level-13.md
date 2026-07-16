# OverTheWire - Bandit: Nivel 13 → 14 - Autenticación SSH con clave privada

## Comando(s)

```bash
scp -P 2220 bandit13@host:/home/bandit13/sshkey.private ~/sshkey.private
```
```bash
chmod 600 ~/sshkey.private
```
```bash
ssh -i ~/sshkey.private bandit14@host -p 2220
```

## Concepto

Una clave privada SSH permite autenticarse como otro usuario. Requiere permisos estrictos.

## Aplicación real

Lateral movement en pentesting: encontrar claves privadas en máquinas comprometidas para pivotar.

## Errores comunes

- Claves con permisos demasiado abiertos; SSH se niega a usarlas.
- Confundir `scp -P` con `ssh -p`.

## Variantes útiles

- `ssh -i key user@host`.
- `scp -P 2220 ...` para puerto no estándar en scp.
