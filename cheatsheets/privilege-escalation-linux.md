# Linux Privilege Escalation Cheatsheet

## Enumeración rápida
```bash
whoami; id; uname -a; cat /etc/os-release
sudo -l
find / -perm -4000 -type f 2>/dev/null
find / -writable -type d 2>/dev/null | grep -v proc
```

## Herramientas
- LinPEAS
- LinEnum
- Linux Smart Enumeration
- GTFOBins
