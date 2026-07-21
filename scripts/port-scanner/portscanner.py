#!/usr/bin/env python3
"""Tiny TCP port scanner (learning scaffold).

Uso ético: solo contra localhost, VMs propias o labs autorizados.
"""

from __future__ import annotations

import argparse
import socket


def parse_port_range(text: str) -> list[int]:
    """Convierte '1-1024' o '22,80,443' en una lista de puertos."""
    text = text.strip()

    if "," in text:
        return [int(part.strip()) for part in text.split(",") if part.strip()]

    if "-" in text:
        start_text, end_text = text.split("-", 1)
        start = int(start_text)
        end = int(end_text)
        if start > end:
            raise ValueError("el puerto inicial no puede ser mayor que el final")
        return list(range(start, end + 1))

    return [int(text)]


def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Devuelve True si el puerto TCP está abierto."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tiny TCP port scanner para aprendizaje en entornos autorizados."
    )
    parser.add_argument("-t", "--target", default="127.0.0.1", help="host objetivo autorizado")
    parser.add_argument("-p", "--ports", default="1-1024", help="rango '1-1024' o lista '22,80,443'")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    ports = parse_port_range(args.ports)

    print(f"Scanning {args.target} ports {args.ports} (authorized lab use only)")
    for port in ports:
        if scan_port(args.target, port):
            print(f"[OPEN] {port}/tcp")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
