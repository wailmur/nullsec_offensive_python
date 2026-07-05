"""
Record type: NS (Name Server)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
An NS record delegates a DNS zone to the authoritative name server(s) responsible for answering queries about that zone. 
This is normally the FIRST query an attacker or pentester makes, because it tells you which server to (attempt to) request a zone transfer (AXFR) from.
Use the axfr.py if you wish to do so.

Run it with:  python3 ns_record.py
"""

import dns.resolver

TARGET_DOMAIN = "zonetransfer.me"


def enumerate_ns_record(domain: str) -> None:
    print(f"[*] Enumerating NS records for: {domain}")
    try:
        answers = dns.resolver.resolve(domain, "NS")
        for rdata in answers:
            print(f"[+] Authoritative name server: {rdata.target}")
    except dns.resolver.NoAnswer:
        print(f"[-] No NS record found for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {domain} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_ns_record(TARGET_DOMAIN)
