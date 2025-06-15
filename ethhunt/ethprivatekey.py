# MIT License (c) 2025 Termux Lab Pro
# YouTube: https://youtube.com/@termuxlabpro
# Telegram: https://t.me/termuxlabpro

import os, time, secrets
from ecdsa import SigningKey, SECP256k1

# === Pure Python Keccak256 (lightweight) ===
class Keccak256:
    def __init__(self):
        self.keccak = __import__('hashlib').new('sha3_256')
    def update(self, x):
        self.keccak.update(x)
    def digest(self):
        return self.keccak.digest()

def banner():
    os.system("clear")
    print("╔════════════════════════════════════╗")
    print("║           T . L . P                ║")
    print("║      Termux Lab Pro                ║")
    print("╚════════════════════════════════════╝")
    print("📺 YT: https://youtube.com/@termuxlabpro")
    print("💬 TG: https://t.me/termuxlabpro")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def generate_ethereum_address():
    priv_key = secrets.token_bytes(32)
    priv_hex = priv_key.hex()

    sk = SigningKey.from_string(priv_key, curve=SECP256k1)
    vk = sk.verifying_key
    pubkey_bytes = b'\x04' + vk.to_string()  # Uncompressed pubkey

    k = Keccak256()
    k.update(pubkey_bytes)
    addr = '0x' + k.digest()[-20:].hex()

    print(f"[🔑] Private: {priv_hex}")
    print(f"[📬] Address: {addr}\n")

if __name__ == "__main__":
    banner()
    while True:
        generate_ethereum_address()
        time.sleep(1)
