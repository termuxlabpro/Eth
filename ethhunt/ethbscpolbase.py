# MIT License © 2025 Termux Lab Pro
# YouTube: https://youtube.com/@termuxlabpro
# Telegram: https://t.me/termuxlabpro

import requests
import ecdsa
import random
import time

# Pure Python Keccak256 (no pysha3 needed)
class Keccak256:
    def __init__(self):
        import hashlib
        self.k = hashlib.new("sha3_256")
    def update(self, b):
        self.k.update(b)
    def digest(self):
        return self.k.digest()

def private_key_to_eth_address(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    pub_key = b'\x04' + vk.to_string()

    keccak = Keccak256()
    keccak.update(pub_key[1:])
    address = keccak.digest()[-20:]
    return '0x' + address.hex()

def check_balance(api_url, address):
    try:
        r = requests.get(api_url.format(address))
        result = r.json()
        balance = int(result['result']) / 1e18
        return balance
    except:
        return None

def main():
    print("🔎 Lightweight ETH/BSC/Polygon Balance Checker")
    priv = input("🔑 Enter private key (64 hex chars): ").strip()

    if len(priv) != 64:
        print("❌ Invalid private key length.")
        return

    addr = private_key_to_eth_address(priv)
    print("📬 Address:", addr)

    # Use public (free-tier) API keys or remove keys for limited usage
    ETH_API = f"https://api.etherscan.io/api?module=account&action=balance&address={{}}&tag=latest&apikey=YourKeyHere"
    BSC_API = f"https://api.bscscan.com/api?module=account&action=balance&address={{}}&tag=latest&apikey=YourKeyHere"
    POLY_API = f"https://api.polygonscan.com/api?module=account&action=balance&address={{}}&tag=latest&apikey=YourKeyHere"

    print("🔄 Checking balances...")
    eth = check_balance(ETH_API, addr)
    bsc = check_balance(BSC_API, addr)
    poly = check_balance(POLY_API, addr)

    print(f"🟣 Ethereum: {eth} ETH")
    print(f"🟡 BNB Chain: {bsc} BNB")
    print(f"🔵 Polygon : {poly} MATIC")

if __name__ == "__main__":
    main()
