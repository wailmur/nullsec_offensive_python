"""
Library used: hashlib (standard library, no install needed)
Target: a single hardcoded MD5 hash, cracked against a small local wordlist (wordlist.txt, about 100 common passwords)

Description
This is a minimal, from-scratch demonstration of how tools like John the Ripper or Hashcat work in "dictionary attack" mode.
For every candidate password in a wordlist, hash it the same way the target hash was produced (MD5 in this exercise) and compare. 
If they match, you've recovered the plaintext.

Instructions
The target hash below is the MD5 hash of the password "p@$$w0rd", which is deliberately included in wordlist.txt so you can find it.
This demonstrates why dictionary/common-password attacks work so well against weak passwords.

Run it with:  python3 password_cracker.py
"""

import hashlib

# MD5 hash of "p@$$w0rd" - this is the "captured" hash we are trying to crack
TARGET_HASH = "b7463760284fd06773ac2a48e29b0acf"
WORDLIST_FILE = "wordlist.txt"


def crack_md5(target_hash: str, wordlist_path: str):
    with open(wordlist_path, "r", encoding="utf-8") as f:
        for line in f:
            candidate = line.strip()
            if not candidate:
                continue

            candidate_hash = hashlib.md5(candidate.encode()).hexdigest()

            if candidate_hash == target_hash:
                return candidate

    return None


if __name__ == "__main__":
    print(f"[*] Target MD5 hash : {TARGET_HASH}")
    print(f"[*] Wordlist        : {WORDLIST_FILE}")
    print("[*] Cracking...\n")

    result = crack_md5(TARGET_HASH, WORDLIST_FILE)

    if result:
        print(f"[+] Password cracked! -> '{result}'")
    else:
        print("[-] Password not found in wordlist")
