"""
AXFR Zone Transfer
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
The specific target we have is misconfigured to allow AXFR (zone transfer). 
A zone transfer dumps EVERY record in the zone at once (A, AAAA, CNAME, MX, NS, SOA, SRV, TXT, etc.), 
which is what the previous scripts queried individually. Basically a jackpot.

Run it in venv with:  python3 axfr.py
"""

import dns.zone
import dns.query
import dns.resolver

TARGET_DOMAIN = "zonetransfer.me"


def attempt_zone_transfer(domain: str) -> None:
    print(f"[*] Step 1: Finding authoritative name servers for {domain}")
    try:
        ns_answers = dns.resolver.resolve(domain, "NS")
    except dns.exception.DNSException as e:
        print(f"[-] Could not resolve NS records: {e}")
        return

    for ns in ns_answers:
        ns_host = str(ns.target).rstrip(".")
        print(f"\n[*] Step 2: Attempting AXFR zone transfer via {ns_host}")
        try:
            ns_ip = dns.resolver.resolve(ns_host, "A")[0].address
            zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=10))
            print(f"[+] Zone transfer SUCCEEDED! Dumping records:\n")
            for name, node in zone.nodes.items():
                rdatasets = node.rdatasets
                for rdataset in rdatasets:
                    print(f"    {name}.{domain}  {rdataset}")
        except Exception as e:
            print(f"[-] Zone transfer failed via {ns_host}: {e}")


if __name__ == "__main__":
    attempt_zone_transfer(TARGET_DOMAIN)
