"""
Record type: CNAME (Canonical Name)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
A CNAME record points one host name to another host name (an alias).
zonetransfer.me has a subdomain "testing.zonetransfer.me" that is a CNAME
alias pointing to "www.zonetransfer.me". 
Could be a testing / staging environment with less protections, 
also could be good if the CNAME points to an expired domain which we can claim and redirect users to our website.

Run it with:  python3 cname_record.py
"""

import dns.resolver

TARGET_HOST = "testing.zonetransfer.me"


def enumerate_cname_record(hostname: str) -> None:
    print(f"[*] Enumerating CNAME records for: {hostname}")
    try:
        answers = dns.resolver.resolve(hostname, "CNAME")
        for rdata in answers:
            print(f"[+] {hostname} -> {rdata.target}")
    except dns.resolver.NoAnswer:
        print(f"[-] No CNAME record found for {hostname}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {hostname} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_cname_record(TARGET_HOST)
