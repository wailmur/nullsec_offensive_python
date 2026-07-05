"""
Library used: socket, threading, queue (all standard library)
Target: localhost / 127.0.0.1 (single machine, no setup required)

Description
An upgrade to port_checker.py: instead of checking one port at a time, this scans a whole range of ports concurrently using a small thread pool,
and looks up the well-known service name for each open port (e.g. 80 -> http) using socket.getservbyport.
The same idea nmap uses for its "service" column, just simpler.

Instructions
Start a couple of throwaway listeners on your own machine first, e.g.:
    python3 -m http.server 8080          # terminal 1
    python3 -m http.server 8081          # terminal 2 (optional)
Then run this script against 127.0.0.1 across a small port range that includes 8080 (open) and other ports (closed) to see the difference.

Run it with:  python3 port_scanner_multithread.py
"""

import socket
import threading
import queue
import time

TARGET_HOST = "127.0.0.1"
PORT_RANGE = range(1, 1025)   # scan well-known ports 1-1024
THREAD_COUNT = 100
TIMEOUT_SECONDS = 0.5

print_lock = threading.Lock()
results = []  # collects (port, service_name) tuples for open ports


def get_service_name(port: int) -> str:
    """Best-effort lookup of the well-known service name for a port."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def worker(host: str, port_queue: "queue.Queue[int]") -> None:
    while True:
        try:
            port = port_queue.get_nowait()
        except queue.Empty:
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT_SECONDS)
            if sock.connect_ex((host, port)) == 0:
                service = get_service_name(port)
                with print_lock:
                    print(f"[+] Port {port:<5} OPEN   ({service})")
                    results.append((port, service))

        port_queue.task_done()


def scan(host: str, ports) -> None:
    port_queue: "queue.Queue[int]" = queue.Queue()
    for port in ports:
        port_queue.put(port)

    threads = []
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=worker, args=(host, port_queue), daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    print(f"[*] Scanning {TARGET_HOST} ports {PORT_RANGE.start}-{PORT_RANGE.stop - 1} "
          f"with {THREAD_COUNT} threads...")
    start_time = time.time()

    scan(TARGET_HOST, PORT_RANGE)

    elapsed = time.time() - start_time
    print(f"\n[*] Scan complete in {elapsed:.2f} seconds. "
          f"{len(results)} open port(s) found.")
    for port, service in sorted(results):
        print(f"    {port}/tcp  {service}")
