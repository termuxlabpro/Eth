import requests
import sys

def check_balance(address, api_key, chain):
    # Determine the correct API URL based on the selected chain for main balance
    if chain == 'eth':
        url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}'
    elif chain == 'bsc':
        url = f'https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}'
    elif chain == 'polygon':
        url = f'https://api.polygonscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}'
    else:
        print("Invalid chain selected.")
        return

    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':
        balance = int(data['result']) / 1e18  # Convert Wei to Ether or equivalent
        print(f"Main Balance for address {address} on {chain.upper()}: {balance} ETH")
    else:
        print("Error:", data['message'])

if __name__ == "__main__":
    # Get the address, API key, and chain from command line arguments
    address = sys.argv[1]
    api_key = sys.argv[2]
    chain = sys.argv[3]
    
    check_balance(address, api_key, chain)
