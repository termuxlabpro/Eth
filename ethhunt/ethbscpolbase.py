"""
MIT License (c) 2025 Termux Lab Pro
YouTube: https://youtube.com/@termuxlabpro
Telegram: https://t.me/termuxlabpro
"""

import requests
from eth_account import Account
from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip44Levels
from colorama import Fore, init
import json

init(autoreset=True)
Account.enable_unaudited_hdwallet_features()

# Constants
DERIVATION_PATHS = [0, 1, 2, 3, 4]  # index for m/44'/60'/0'/0/i
CHAINS = {
    "Ethereum": {
        "coin": Bip44Coins.ETHEREUM,
        "api_balance": "https://api.etherscan.io/api",
        "api_nft": "https://api.etherscan.io/api",
        "api_key": "YourEtherscanAPIKey"
    },
    "BSC": {
        "coin": Bip44Coins.BINANCE_SMART_CHAIN,
        "api_balance": "https://api.bscscan.com/api",
        "api_nft": "https://api.bscscan.com/api",
        "api_key": "YourBscscanAPIKey"
    },
    "Polygon": {
        "coin": Bip44Coins.POLYGON,
        "api_balance": "https://api.polygonscan.com/api",
        "api_nft": "https://api.polygonscan.com/api",
        "api_key": "YourPolygonscanAPIKey"
    },
    "Base": {
        # Base network currently does not have official scan API similar to above.
        # You may need to replace with a valid Base block explorer API or your own RPC queries.
        "coin": Bip44Coins.ETHEREUM,
        "api_balance": "https://api.basescan.org/api",
        "api_nft": "https://api.basescan.org/api",
        "api_key": "YourBaseScanAPIKey"
    }
}

def generate_address_from_privkey(privkey_hex, coin, account_index):
    # Bip44 wallet from private key
    bip44_mst = Bip44.FromPrivateKey(bytes.fromhex(privkey_hex), coin)
    addr_obj = bip44_mst.Change(Bip44Changes.CHAIN_EXT).AddressIndex(account_index)
    return addr_obj.PublicKey().ToAddress()

def check_balance(api_url, address, api_key):
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "apikey": api_key,
        "tag": "latest"
    }
    try:
        response = requests.get(api_url, params=params, timeout=10)
        result = response.json()
        if result["status"] == "1":
            balance_wei = int(result["result"])
            balance_eth = balance_wei / 1e18
            return balance_eth
        else:
            return None
    except Exception as e:
        print(f"{Fore.RED}Error checking balance: {e}")
        return None

def check_nfts(api_url, address, api_key):
    # Etherscan-like API does not provide standard NFT info.
    # You may want to use Moralis or Alchemy NFT APIs for this, which need API keys.
    # For simplicity, placeholder function returning empty list
    return []

def main():
    print(Fore.CYAN + "=== Termux Lab Pro ETH/BSC/Polygon/Base Scanner ===")
    privkey = input("Enter your Ethereum Private Key (hex): ").strip()
    if len(privkey) != 64:
        print(Fore.RED + "Invalid private key length.")
        return
    
    results = []

    for chain_name, info in CHAINS.items():
        print(Fore.YELLOW + f"\n--- Scanning {chain_name} network ---")
        for i in DERIVATION_PATHS:
            try:
                addr = generate_address_from_privkey(privkey, info["coin"], i)
            except Exception as e:
                print(f"{Fore.RED}Failed to generate address for index {i} on {chain_name}: {e}")
                continue

            balance = check_balance(info["api_balance"], addr, info["api_key"])
            nfts = check_nfts(info["api_nft"], addr, info["api_key"])

            print(Fore.GREEN + f"Path m/44'/60'/0'/0/{i} - Address: {addr}")
            print(f"Balance: {balance} {chain_name}")
            print(f"NFTs found: {len(nfts)}")

            results.append({
                "chain": chain_name,
                "index": i,
                "address": addr,
                "balance": balance,
                "nfts": nfts
            })

    # Optionally save results to file
    with open("scan_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print(Fore.CYAN + "\nScan completed. Results saved to scan_results.json")

if __name__ == "__main__":
    main()
