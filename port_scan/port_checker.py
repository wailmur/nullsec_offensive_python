"""
Library used: socket (standard library, no install needed)
Target: localhost / 127.0.0.1 (run on host machine, no setup required)

Description
The simplest possible way to check if a single TCP port is open on a host. 
Attempts a TCP connect() and see if it succeeds.

This is the foundation that the multithreaded scanner ("port_scanner_multithread.py") builds on.

Instructions
Start a listener on your own machine so there's something to find, e.g. in one terminal:
    python3 -m http.server 8080
Then in another terminal run this script against 127.0.0.1 port 8080 (open) and port 9999 (closed) to see both outcomes.

Run it with:  python3 port_checker.py
"""

import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8080     # change this to test different ports
TIMEOUT_SECONDS = 1.0


def check_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if the TCP port is open, False otherwise."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        # connect_ex returns 0 on success instead of raising an exception
        result = sock.connect_ex((host, port))
        return result == 0


if __name__ == "__main__":
    print(f"[*] Checking {TARGET_HOST}:{TARGET_PORT} ...")
    if check_port(TARGET_HOST, TARGET_PORT, TIMEOUT_SECONDS):
        print(f"[+] Port {TARGET_PORT} is OPEN")
    else:
        print(f"[-] Port {TARGET_PORT} is CLOSED or filtered")
