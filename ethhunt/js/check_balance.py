import requests
import sys

def get_balance(address, api_key, chain):
    if chain == 'eth':
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    elif chain == 'bsc':
        url = f"https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    elif chain == 'polygon':
        url = f"https://api.polygonscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    else:
        print("Unsupported chain")
        return

    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        balance = int(data['result']) / 10**18  # Convert balance to Ether
        print(f"Balance: {balance:.18f}")
    else:
        print("Error fetching balance:", data['message'])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python check_balance.py <address> <api_key> <chain>")
        sys.exit(1)

    address = sys.argv[1]
    api_key = sys.argv[2]
    chain = sys.argv[3]

    get_balance(address, api_key, chain)
