# Nmap Cheatsheet

## Escaneos comunes
```bash
nmap -sT -p- -T4 target
nmap -sV -sC -O -p- target
nmap -sU --top-ports 100 target
nmap -A -T4 target
```

## Output
```bash
nmap -oA output target
```
