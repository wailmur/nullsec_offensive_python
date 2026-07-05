"""
Record type: TXT (Text)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
A TXT record stores arbitrary human-readable text in DNS. 
Organizations use it for things like domain-verification tokens (Google, GoDaddy, etc.)
and SPF records, but sometimes it accidentally leaks sensitive info such as internal contact details.
zonetransfer.me deliberately includes a TXT record with a contact phone number/email as a teaching example of exactly this kind of information leakage.

Run it with:  python3 txt_record.py
"""

import dns.resolver

TARGET_HOST = "zonetransfer.me"


def enumerate_txt_record(hostname: str) -> None:
    print(f"[*] Enumerating TXT records for: {hostname}")
    try:
        answers = dns.resolver.resolve(hostname, "TXT")
        for rdata in answers:
            # TXT records can be split into multiple byte-strings; join them
            text = b"".join(rdata.strings).decode(errors="replace")
            print(f"[+] TXT: {text}")
    except dns.resolver.NoAnswer:
        print(f"[-] No TXT record found for {hostname}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {hostname} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_txt_record(TARGET_HOST)
