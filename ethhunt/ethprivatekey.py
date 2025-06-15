import os
import time
import secrets
import binascii
import hashlib
from ecdsa import SigningKey, SECP256k1

def banner():
    os.system("clear")
    art = [
        "████████╗██╗     ██████╗ ",
        "╚══██╔══╝██║     ██╔══██╗",
        "   ██║   ██║     ██████╔╝",
        "   ██║   ██║     ██╔═══╝ ",
        "   ██║   ███████╗██║     ",
        "   ╚═╝   ╚══════╝╚═╝     ",
        "\n╔═══════════════════════════════╗",
        "║         T . L . P             ║",
        "║     Termux Lab Pro            ║",
        "╚═══════════════════════════════╝",
        "📺 YouTube : https://youtube.com/@termuxlabpro",
        "💬 Telegram: https://t.me/termuxlabpro",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    ]
    for line in art:
        print(line)
        time.sleep(0.05)

def keccak256(data):
    """Compute the Keccak-256 hash."""
    keccak = hashlib.new('sha3_256')
    keccak.update(data)
    return keccak.digest()

def priv_to_eth(priv_hex):
    """Convert a hexadecimal private key to an Ethereum address."""
    # Convert the private key from hex to bytes
    private_key_bytes = binascii.unhexlify(priv_hex)
    # Generate the public key using ECDSA
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key_bytes = sk.get_verifying_key().to_string()
    # Hash the public key to get the Ethereum address
    keccak_hash = keccak256(b'\x04' + public_key_bytes)  # Prepend 0x04 for uncompressed public key
    eth_address = "0x" + keccak_hash[-20:].hex()
    return eth_address

def main():
    banner()
    while True:
        # Generate a random private key
        priv = secrets.token_hex(32)  # Generate a random 32-byte private key
        addr = priv_to_eth(priv)  # Convert the private key to an Ethereum address
        print(f"[🔑] Private Key: {priv}")  # Show the private key
        print(f"[📬] Ethereum Address: {addr}")  # Show the generated Ethereum address
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        time.sleep(1)

if __name__ == "__main__":
    main()
