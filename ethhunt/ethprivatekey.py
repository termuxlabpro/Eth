# MIT License (c) 2025 Termux Lab Pro
# YouTube: https://youtube.com/@termuxlabpro
# Telegram: https://t.me/termuxlabpro

import os, time, secrets, binascii
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak
from colorama import Fore, init

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
        time.sleep(0.05)

def priv_to_eth(priv_hex):
    private_key_bytes = binascii.unhexlify(priv_hex)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key().to_string()
    public_key_bytes = b"\x04" + vk
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes[1:])
    eth_address = "0x" + keccak_hash.digest()[-20:].hex()
    return eth_address

def main():
    banner()
    while True:
        priv = secrets.token_hex(32)
        addr = priv_to_eth(priv)
        print(f"{Fore.YELLOW}[🔑] Private: {Fore.GREEN}{priv}")
        print(f"{Fore.YELLOW}[📬] Address: {Fore.CYAN}{addr}")
        print(Fore.MAGENTA + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        time.sleep(1)

if __name__ == "__main__":
    main()
