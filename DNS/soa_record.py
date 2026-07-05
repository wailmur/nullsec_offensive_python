"""
Record type: SOA (Start of Authority)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
The SOA record defines the authoritative information for a zone:
1. which server is the primary source of truth
2. who the administrative contact is,
3. timing values used by secondary name servers (refresh/retry/expire/minimum TTL). 
It's small but useful during recon and for understanding zone replication.

Run it with:  python3 soa_record.py
"""

import dns.resolver

TARGET_DOMAIN = "zonetransfer.me"


def enumerate_soa_record(domain: str) -> None:
    print(f"[*] Enumerating SOA record for: {domain}")
    try:
        answers = dns.resolver.resolve(domain, "SOA")
        for rdata in answers:
            print(f"[+] Primary name server : {rdata.mname}")
            print(f"[+] Admin email (as host): {rdata.rname}")
            print(f"[+] Serial              : {rdata.serial}")
            print(f"[+] Refresh (sec)       : {rdata.refresh}")
            print(f"[+] Retry (sec)         : {rdata.retry}")
            print(f"[+] Expire (sec)        : {rdata.expire}")
            print(f"[+] Minimum TTL (sec)   : {rdata.minimum}")
    except dns.resolver.NoAnswer:
        print(f"[-] No SOA record found for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {domain} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_soa_record(TARGET_DOMAIN)
