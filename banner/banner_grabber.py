"""
Library used: socket (standard library, no install needed)
Target: localhost / 127.0.0.1 (single machine, no setup required)

Description
"Banner grabbing" means connecting to an open port and reading whatever
data the service sends back (or sending a small probe and reading the
reply), to identify what software/version is running.

Set up your own local server to test on:
Start a simple HTTP server on your own machine so there's a real banner to grab:
    python3 -m http.server 8080
Then run this script against 127.0.0.1:8080. It sends a minimal HTTP
HEAD request and prints the response headers, which reveal the server
software (e.g. "Server: SimpleHTTP/0.6 Python/3.x").

Run it with:  python3 banner_grabber.py
"""

import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8080
TIMEOUT_SECONDS = 3.0


def grab_banner(host: str, port: int, timeout: float = 3.0) -> str:
    """Connect to host:port, send a small probe, and return whatever
    text the service responds with."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))

        # A minimal HTTP request works well for web servers. Many other services (SSH, FTP, SMTP) send a banner immediately on connect without needing any request at all.
        # you can try commenting the next two lines out against an SSH/FTP port to see that in action.
        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())

        data = b""
        try:
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass  # some services keep the connection open, which is fine

        return data.decode(errors="replace")


if __name__ == "__main__":
    print(f"[*] Grabbing banner from {TARGET_HOST}:{TARGET_PORT} ...")
    try:
        banner = grab_banner(TARGET_HOST, TARGET_PORT, TIMEOUT_SECONDS)
        if banner:
            print("[+] Banner received:\n")
            print(banner)
        else:
            print("[-] No data received (service may not respond to this probe)")
    except (ConnectionRefusedError, socket.timeout) as e:
        print(f"[-] Could not connect: {e}")
