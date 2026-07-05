"""
Record type: AAAA (IPv6 Address)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
Same thing as a_record.py before but for IPv6

Run it in venv with:  python3 aaaa_record.py
"""

import dns.resolver

# This specific subdomain is the one zonetransfer.me uses to demonstrate
# an AAAA record (see the answer sheet for details).
TARGET_HOST = "ipv6actnow.org.zonetransfer.me"


def enumerate_aaaa_record(hostname: str) -> None:
    print(f"[*] Enumerating AAAA (IPv6) records for: {hostname}")
    try:
        answers = dns.resolver.resolve(hostname, "AAAA")
        for rdata in answers:
            print(f"[+] {hostname} -> {rdata.address}")
    except dns.resolver.NoAnswer:
        print(f"[-] No AAAA record found for {hostname}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {hostname} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_aaaa_record(TARGET_HOST)
