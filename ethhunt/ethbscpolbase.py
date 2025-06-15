# MIT License © 2025 Termux Lab Pro
# YouTube: https://youtube.com/@termuxlabpro
# Telegram: https://t.me/termuxlabpro

import os, random, hashlib, requests
from colorama import Fore, init
init(autoreset=True)

def banner():
    os.system("clear")
    print(Fore.GREEN + "████████╗██╗     ██████╗ ")
    print("╚══██╔══╝██║     ██╔══██╗")
    print("   ██║   ██║     ██████╔╝")
    print("   ██║   ██║     ██╔═══╝ ")
    print("   ██║   ███████╗██║     ")
    print("   ╚═╝   ╚══════╝╚═╝     ")
    print(Fore.CYAN + "\n╔═══════════════════════════════╗")
    print(Fore.CYAN + "║         " + Fore.MAGENTA + "T . L . P" + Fore.CYAN + "             ║")
    print(Fore.CYAN + "║     Termux Lab Pro            ║")
    print(Fore.CYAN + "╚═══════════════════════════════╝")
    print(Fore.YELLOW + "📺 YouTube : @termuxlabpro")
    print(Fore.YELLOW + "💬 Telegram: t.me/termuxlabpro\n")

def generate_private_key():
    return ''.join(random.choice("0123456789abcdef") for _ in range(64))

def private_key_to_address(private_key_hex):
    from ecdsa import SigningKey, SECP256k1
    priv_bytes = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()
    pub_key = b'\x04' + vk.to_string()
    keccak = hashlib.new('sha3_256', pub_key[1:]).digest()
    return '0x' + keccak[-20:].hex()

def check_balance(apis, address):
    for api in apis:
        try:
            url = api.format(address=address)
            res = requests.get(url, timeout=10)
            data = res.json()
            if "result" in data:
                if isinstance(data["result"], str):
                    return int(data["result"], 16) / 1e18
                elif isinstance(data["result"], dict) and "balance" in data["result"]:
                    return int(data["result"]["balance"], 16) / 1e18
        except: continue
    return 0

def main():
    banner()
    chains = {
        "Ethereum": [
            "https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken",
            "https://eth.llamarpc.com/api?module=account&action=balance&address={address}&tag=latest"
        ],
        "BSC": [
            "https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey=YourApiKeyToken"
        ],
        "Polygon": [
            "https://api.polygonscan.com/api?module=account&action=balance&address={address}&apikey=YourApiKeyToken"
        ],
        "Base": [
            "https://base.blockscout.com/api?module=account&action=balance&address={address}"
        ]
    }

    while True:
        priv = generate_private_key()
        addr = private_key_to_address(priv)
        print(Fore.CYAN + f"[🔑] Private: {priv}")
        print(Fore.YELLOW + f"[📬] Address: {addr}")
        found = False

        for chain, apis in chains.items():
            bal = check_balance(apis, addr)
            if bal > 0:
                print(Fore.GREEN + f"[💰] {chain}: {bal}")
                found = True
            else:
                print(Fore.RED + f"[✘] {chain}: 0")

        if found:
            with open("found_keys.txt", "a") as f:
                f.write(f"{priv} -> {addr}\n")

if __name__ == "__main__":
    main()
