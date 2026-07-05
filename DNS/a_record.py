"""
Record type: A (IPv4 Address)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Desciption
This script asks a DNS resolver for the A record(s) of a target host and prints the resulting IP address(es).
We use it to bypass WAF / Rate limiting present on a domain, making some attacks possible.

Run it in venv with:  python3 a_record.py
"""

import dns.resolver

# Any hostname under zonetransfer.me can be swapped in here.
TARGET_HOST = "zonetransfer.me"


def enumerate_a_record(hostname: str) -> None:
    print(f"[*] Enumerating A (IPv4) records for: {hostname}")
    try:
        answers = dns.resolver.resolve(hostname, "A")
        for rdata in answers:
            print(f"[+] {hostname} -> {rdata.address}")
    except dns.resolver.NoAnswer:
        print(f"[-] No A record found for {hostname}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {hostname} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_a_record(TARGET_HOST)
