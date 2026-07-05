"""
Record type: SRV (Service)
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
An SRV record locates hosts providing a specific service, such as a SIP (VoIP) endpoint. 
zonetransfer.me publishes an SRV record for SIP at "_sip._tcp.zonetransfer.me". 
SRV records reveal the protocol, target host, and port a service runs on, useful for mapping internal infrastructure.
Alternative to nmap or port scanning python script for knowing if certain services running.

Run it with:  python3 srv_record.py
"""

import dns.resolver

# SRV record names follow the format: _service._protocol.domain
TARGET_SRV = "_sip._tcp.zonetransfer.me"


def enumerate_srv_record(srv_name: str) -> None:
    print(f"[*] Enumerating SRV records for: {srv_name}")
    try:
        answers = dns.resolver.resolve(srv_name, "SRV")
        for rdata in answers:
            print(f"[+] priority={rdata.priority} weight={rdata.weight} "
                  f"port={rdata.port} target={rdata.target}")
    except dns.resolver.NoAnswer:
        print(f"[-] No SRV record found for {srv_name}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] {srv_name} does not exist")
    except dns.exception.DNSException as e:
        print(f"[-] DNS error: {e}")


if __name__ == "__main__":
    enumerate_srv_record(TARGET_SRV)
