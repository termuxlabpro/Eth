# MIT License © 2025 Termux Lab Pro
# YouTube: https://youtube.com/@termuxlabpro
# Telegram: https://t.me/termuxlabpro

import requests, ecdsa, time, random

# Custom pure-Python Keccak256
class Keccak256:
    def __init__(self):
        import hashlib
        self.k = hashlib.new("sha3_256")
    def update(self, b):
        self.k.update(b)
    def digest(self):
        return self.k.digest()

def private_key_to_address(private_key_hex):
    priv_bytes = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(priv_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    pub_key = b'\x04' + vk.to_string()
    keccak = Keccak256()
    keccak.update(pub_key[1:])
    addr = keccak.digest()[-20:]
    return '0x' + addr.hex()

def check_balance(api_url, address):
    try:
        r = requests.get(api_url.format(address), timeout=10)
        res = r.json()
        if res["status"] == "1":
            return int(res["result"]) / 1e18
    except: pass
    return None

def main():
    print("🔍 ETH/BSC/POLYGON/BASE Private Key Hunter - T.L.P")

    # Add your free API keys here (or remove for limited usage)
    ETH = "https://api.etherscan.io/api?module=account&action=balance&address={}&tag=latest&apikey=YourKeyHere"
    BSC = "https://api.bscscan.com/api?module=account&action=balance&address={}&tag=latest&apikey=YourKeyHere"
    POLY = "https://api.polygonscan.com/api?module=account&action=balance&address={}&tag=latest&apikey=YourKeyHere"
    BASE = "https://api.basescan.org/api?module=account&action=balance&address={}&tag=latest&apikey=YourKeyHere"

    while True:
        priv = ''.join(random.choice('0123456789abcdef') for _ in range(64))
        addr = private_key_to_address(priv)

        eth = check_balance(ETH, addr)
        bsc = check_balance(BSC, addr)
        poly = check_balance(POLY, addr)
        base = check_balance(BASE, addr)

        has_balance = any(x and x > 0 for x in [eth, bsc, poly, base])

        print(f"\n🔑 Private: {priv}")
        print(f"📬 Address: {addr}")
        print(f"🟣 ETH: {eth}  🟡 BNB: {bsc}  🔵 MATIC: {poly}  🟠 BASE: {base}")

        if has_balance:
            print("💰 FOUND! Save this key.")
            with open("hit.txt", "a") as f:
                f.write(f"{priv} -> {addr}\n")
        time.sleep(1)

if __name__ == "__main__":
    main()
