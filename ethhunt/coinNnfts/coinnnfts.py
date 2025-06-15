"""
MIT License (c) 2025 Termux Lab Pro
YouTube: https://youtube.com/@termuxlabpro
Telegram: https://t.me/termuxlabpro
"""

import os
import requests
import time
import ecdsa
from colorama import Fore, init
from eth_utils import to_checksum_address, keccak

init(autoreset=True)

def display_banner():
    os.system("clear")
    banner_art = [
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
    for line in banner_art:
        print(line)
        time.sleep(0.05)

def create_private_key():
    return os.urandom(32).hex()  # Generate a random 32-byte private key

def derive_public_key(priv_hex):
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(priv_hex), curve=ecdsa.SECP256k1)
    verifying_key = signing_key.verifying_key
    return verifying_key.to_string()

def generate_address_from_public_key(pubkey_bytes):
    keccak_hash = keccak(pubkey_bytes)
    return to_checksum_address('0x' + keccak_hash.hex()[-40:])

def check_balance_etherscan(addr, api_key):
    response = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey={api_key}", timeout=10)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return int(result["result"]) / 1e18
    raise Exception("Etherscan API Error")

def check_balance_bscscan(addr, api_key):
    response = requests.get(f"https://api.bscscan.com/api?module=account&action=balance&address={addr}&tag=latest&apikey={api_key}", timeout=10)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return int(result["result"]) / 1e18
    raise Exception("BSCScan API Error")

def check_balance_polygon(addr, api_key):
    response = requests.get(f"https://api.polygonscan.com/api?module=account&action=balance&address={addr}&tag=latest&apikey={api_key}", timeout=10)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return int(result["result"]) / 1e18
    raise Exception("PolygonScan API Error")

def check_nfts_etherscan(addr, api_key):
    response = requests.get(f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={addr}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}", timeout=10)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return result['result']
    raise Exception("Etherscan NFT API Error")

def check_nfts_bscscan(addr, api_key):
    response = requests.get(f"https://api.bscscan.com/api?module=account&action=tokennfttx&address={addr}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}", timeout=10)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return result['result']
    raise Exception("BSCScan NFT API Error")

def check_nfts_polygon(addr, api_key):
    response = requests.get(f"https://api.polygonscan.com/api?module=account&action=tokennfttx&address={addr}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}", timeout=10)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            return result['result']
    raise Exception("PolygonScan NFT API Error")

def retrieve_balances_and_nfts(addr, api_keys):
    balances = {}

    try:
        balances['Ethereum'] = check_balance_etherscan(addr, api_keys['etherscan'])  # Check Ethereum balance
    except Exception as e:
        print(Fore.RED + f"Etherscan API error for {addr}: {e}")
        balances['Ethereum'] = None

    try:
        balances['BNB Smart Chain'] = check_balance_bscscan(addr, api_keys['bscscan'])  # Check BNB Smart Chain balance
    except Exception as e:
        print(Fore.RED + f"BSCScan API error for {addr}: {e}")
        balances['BNB Smart Chain'] = None

    try:
        balances['Polygon'] = check_balance_polygon(addr, api_keys['polygon'])  # Check Polygon balance
    except Exception as e:
        print(Fore.RED + f"PolygonScan API error for {addr}: {e}")
        balances['Polygon'] = None

    nfts = {}
    try:
        nfts['Ethereum'] = check_nfts_etherscan(addr, api_keys['etherscan'])  # Check Ethereum NFTs
    except Exception as e:
        print(Fore.RED + f"Etherscan NFT API error for {addr}: {e}")
        nfts['Ethereum'] = None

    try:
        nfts['BNB Smart Chain'] = check_nfts_bscscan(addr, api_keys['bscscan'])  # Check BNB Smart Chain NFTs
    except Exception as e:
        print(Fore.RED + f"BSCScan NFT API error for {addr}: {e}")
        nfts['BNB Smart Chain'] = None

    try:
        nfts['Polygon'] = check_nfts_polygon(addr, api_keys['polygon'])  # Check Polygon NFTs
    except Exception as e:
        print(Fore.RED + f"PolygonScan NFT API error for {addr}: {e}")
        nfts['Polygon'] = None

    return balances, nfts  # Return the balances and NFTs dictionaries

def log_found_key(priv, addresses, balances, nfts):
    with open("eth.txt", "a") as file:  # Log to eth.txt
        file.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        file.write(f"Private Key     : {priv}\n")
        for label in addresses:
            file.write(f"{label}: {addresses[label]}\n")
            file.write(f" └─ Balance: {balances[label]} {'ETH' if label == 'Ethereum' else ''}\n")
        for chain, nft_list in nfts.items():
            if nft_list:
                file.write(f" └─ {chain} NFTs: {len(nft_list)} found\n")
                for nft in nft_list:
                    file.write(f"    - Token ID: {nft['tokenID']}, Contract: {nft['contractAddress']}\n")
            else:
                file.write(f" └─ {chain} NFTs: No valid NFTs found\n")
        file.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

def scan_for_keys(api_keys):
    priv_key = create_private_key()
    print(Fore.YELLOW + "[+] Private Key:", priv_key)

    pub_key = derive_public_key(priv_key)
    addr = generate_address_from_public_key(pub_key)

    addresses = {
        "Ethereum Address": addr,
    }

    balances, nfts = retrieve_balances_and_nfts(addr, api_keys)

    for chain, balance in balances.items():
        if balance is None:
            print(Fore.YELLOW + f"[{addr}]")
            print(Fore.YELLOW + f" └─ {chain} Balance: No valid balance found ❌")
        else:
            color = Fore.GREEN if balance > 0 else Fore.RED
            print(color + f"[{addr}]")
            print(color + f" └─ {chain} Balance: {balance} {'ETH' if chain == 'Ethereum' else ''}\n")
        
    for chain, nft_list in nfts.items():
        if nft_list is None or len(nft_list) == 0:
            print(Fore.YELLOW + f"[{addr}]")
            print(Fore.YELLOW + f" └─ {chain} NFTs: No valid NFTs found ❌")
        else:
            print(Fore.GREEN + f"[{addr}]")
            print(Fore.GREEN + f" └─ {chain} NFTs: {len(nft_list)} found ✅")
            for nft in nft_list:
                print(Fore.GREEN + f"    - Token ID: {nft['tokenID']}, Contract: {nft['contractAddress']}")

    if any(balance and balance > 0 for balance in balances.values()) or any(len(nft_list) > 0 for nft_list in nfts.values()):
        log_found_key(priv_key, addresses, balances, nfts)

    print(Fore.BLUE + "🔁 Scanning for the next key...\n")
    time.sleep(2)

def main():
    api_keys = {}
    api_keys['etherscan'] = input(Fore.YELLOW + "Enter your Etherscan API Key: ")
    api_keys['bscscan'] = input(Fore.YELLOW + "Enter your BSCScan API Key: ")
    api_keys['polygon'] = input(Fore.YELLOW + "Enter your PolygonScan API Key: ")

    display_banner()
    while True:
        scan_for_keys(api_keys)

if __name__ == "__main__":
    main()
