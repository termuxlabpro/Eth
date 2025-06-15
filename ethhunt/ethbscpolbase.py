# MIT License (c) 2025 Termux Lab Pro
# YouTube: https://youtube.com/@termuxlabpro
# Telegram: https://t.me/termuxlabpro

import os, time, secrets, requests
from hashlib import sha3_256
from colorama import Fore, init
from ecdsa import SigningKey, SECP256k1

init(autoreset=True)

def banner():
    os.system("clear")
    art = [
        Fore.GREEN + "████████╗██╗     ██████╗ ",
        "╚══██╔══╝██║     ██╔══██╗",
        "   ██║   ██║     ██████╔╝",
        "   ██║   ██║     ██╔═══╝ ",
        "   ██║   ███████╗██║     ",
        "   ╚═╝   ╚══════╝╚═╝     ",
        Fore.CYAN + "\n╔═══════════════════════════════╗",
        Fore.CYAN + "║         " + Fore.MAGENTA + "T . L . P" + Fore.CYAN + "             ║",
        Fore.CYAN + "║     Termux Lab Pro            ║",
        Fore.CYAN + "╚═══════════════════════════════╝",
        Fore.YELLOW + "📺 YouTube : https://youtube.com/@termuxlabpro",
        Fore.YELLOW + "💬 Telegram: https://t.me/termuxlabpro",
        Fore.MAGENTA + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    ]
    for line in art:
        print(line)
        time.sleep(0.02)

def generate_eth_address():
    private_key = secrets.token_hex(32)
    sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
    vk = sk.verifying_key.to_string()
    pub_key = b'\x04' + vk
    keccak = sha3_256()
    keccak.update(pub_key)
    eth_address = '0x' + keccak.hexdigest()[-40:]
    return private_key, eth_address

def get_eth_balance(address):
    try:
        r = requests.get(f"https://api.ethplorer.io/getAddressInfo/{address}?apiKey=freekey", timeout=10)
        data = r.json()
        balance = data.get("ETH", {}).get("balance", 0)
        return float(balance)
    except:
        return 0

def main():
    banner()
    while True:
        priv, addr = generate_eth_address()
        print(Fore.CYAN + f"🔑 Private: {priv}")
        print(Fore.YELLOW + f"📬 Address: {addr}")

        balance = get_eth_balance(addr)
        if balance > 0:
            print(Fore.GREEN + f"💰 Balance: {balance} ETH ✅")
            with open("eth_found.txt", "a") as f:
                f.write(f"Private: {priv}\nAddress: {addr}\nBalance: {balance} ETH\n{'='*40}\n")
        else:
            print(Fore.RED + "💸 Balance: 0 ETH")
        time.sleep(1)

if __name__ == "__main__":
    main()
