"""
Record type: MX (Mail Exchange)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
An MX record points to the mail server(s) responsible for accepting email for a domain, 
along with a priority value (lower = tried first). 
Knowing which mail provider a target uses (e.g. Google Workspace) is useful for phishing.

Run it with:  python3 mx_record.py
"""

import dns.resolver

TARGET_DOMAIN = "zonetransfer.me"


def enumerate_mx_record(domain: str) -> None:
    print(f"[*] Enumerating MX records for: {domain}")
    try:
        answers = dns.resolver.resolve(domain, "MX")
        # Sort by priority (preference) so results are easy to read
        for rdata in sorted(answers, key=lambda r: r.preference):
            print(f"[+] priority={rdata.preference:<3} mail server={rdata.exchange}")
    except dns.resolver.NoAnswer:
        print(f"[-] No MX record found for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {domain} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_mx_record(TARGET_DOMAIN)
