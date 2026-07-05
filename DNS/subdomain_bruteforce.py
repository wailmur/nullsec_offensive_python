"""
Library used: dnspython (pip install dnspython)
Legal target: zonetransfer.me

Description
Given a top-level domain and NO prior knowledge of its subdomains, this script tries a wordlist of common subdomain names 
(admin, test, www, vpn, staging, etc.) prefixed onto the domain, and checks whether each one resolves. 
This is exactly how tools like gobuster, ffuf, or dnsenum's "dictionary mode" work under the hood, just simplified and single threaded for teaching clarity.
Don't worry about how threading works, we might explain later, or just search online or something.

Run against zonetransfer.me, this script should find "testing" purely by guessing, without ever knowing in advance that it exists (unlike the CNAME script from earlier, which already knew the exact name).

This method is ACTIVE
Brute-forcing is "active" recon as you are sending a flood of DNS queries, which is noisy, slow, and can only ever find subdomains that happen to be in your wordlist. 
There are better, quieter, more complete techniques see the comment block at the bottom of this file for a summary.

Run it with:  python3 subdomain_bruteforce.py
"""

import dns.resolver
import concurrent.futures

TARGET_DOMAIN = "zonetransfer.me"
THREAD_COUNT = 20

# A small demonstration wordlist. Real tools ship lists with 10,000-100,000+
# entries (e.g. SecLists' subdomains-top1million-*.txt).
SUBDOMAIN_WORDLIST = [
    "www", "mail", "ftp", "admin", "test", "testing", "dev", "staging",
    "vpn", "portal", "remote", "webmail", "api", "app", "beta", "shop",
    "blog", "cpanel", "autodiscover", "owa", "office", "internal",
    "intranet", "secure", "sso", "git", "jenkins", "monitor", "status",
    "support", "help", "docs", "cdn", "static", "assets", "media",
    "images", "download", "files", "backup", "old", "new", "demo",
    "sandbox", "uat", "qa", "prod", "production", "db", "database",
]


def resolves(hostname: str) -> bool:
    """Return True if the hostname resolves to an A record."""
    try:
        dns.resolver.resolve(hostname, "A")
        return True
    except dns.exception.DNSException:
        return False


def check_candidate(subdomain: str, domain: str):
    fqdn = f"{subdomain}.{domain}"
    if resolves(fqdn):
        return fqdn
    return None


def bruteforce_subdomains(domain: str, wordlist):
    found = []
    print(f"[*] Brute-forcing {len(wordlist)} candidate subdomains of {domain} "
          f"with {THREAD_COUNT} threads...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as pool:
        futures = {pool.submit(check_candidate, sub, domain): sub for sub in wordlist}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"[+] Found: {result}")
                found.append(result)

    return found


if __name__ == "__main__":
    results = bruteforce_subdomains(TARGET_DOMAIN, SUBDOMAIN_WORDLIST)
    print(f"\n[*] Done. {len(results)} subdomain(s) found:")
    for r in sorted(results):
        print(f"    {r}")

# Alternative tech that I couldn't cover in the interest of time or because I'm lazy:
# 1. Certificate Transparency logs 
#    - passive, very effective, no DNS queries sent to the target at all.
#      every publicly-trusted TLS certificate is logged publicly. 
#      Searching https://crt.sh/?q=%25.zonetransfer.me shows every subdomain that has ever had a certificate issued for it
#      Finds things a wordlist never would (e.g. "asfdbauthdns").
#
# 2. Search engine / OSINT dorking
#    - "site:*.zonetransfer.me" style queries,
#      or dedicated OSINT tools (theHarvester, Shodan, Censys)
#      that index hostnames they've already seen.
#
# 3. Zone transfer (see axfr.py)
#    - If AXFR is open, this gives you every subdomain at once with zero guessing. 
#      Which is exactly why zonetransfer.me is a bad (deliberately, for teaching) example to brute-force against
#      In the real world most servers block AXFR, which is why brute-forcing and cert transparency matter.
#
# 4. Passive DNS databases (e.g. SecurityTrails, VirusTotal's passive DNS)
#    - historical records of what a domain has resolved to over time, run by
#      third parties who've already been recording internet DNS traffic.
# You can use any of these depending on the situation. Brute forcing still has its place where all these other methods fail.
