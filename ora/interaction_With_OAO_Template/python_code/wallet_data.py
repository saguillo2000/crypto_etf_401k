import json
import os 
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Load tokens from JSON file
with open('tokens.json', 'r') as file:
    tokens = json.load(file)

infura_url = os.getenv('URL_RPC')
web3 = Web3(Web3.HTTPProvider(infura_url))

wallet_address = os.getenv('PUBLIC_KEY')

# ABI for ERC20 tokens (balanceOf and decimals functions)
token_abi = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

def get_token_balance(token):
    token_contract = web3.eth.contract(address=token['address'], abi=token_abi)
    
    balance = token_contract.functions.balanceOf(wallet_address).call()
    decimals = token_contract.functions.decimals().call()
    
    adjusted_balance = balance / (10 ** decimals)
    return adjusted_balance

def get_eth_balance():
    balance_wei = web3.eth.get_balance(wallet_address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    return balance_eth

print(f"Wallet address: {wallet_address}")
print("Token Information and Balances:")

# Get ETH balance
try:
    eth_balance = get_eth_balance()
    eth_info = {
        "symbol": "ETH",
        "name": "Ethereum",
        "address": "Native Currency",
        "description": "The native currency of the Ethereum network.",
        "balance": f"{eth_balance:.4f}" if eth_balance > 0 else "N/A"
    }
    print(json.dumps(eth_info, indent=2))
except Exception as e:
    print(f"Error fetching ETH balance: {str(e)}")

# Get and print token balances
for token in tokens:
    try:
        balance = get_token_balance(token)
        token_info = {
            "symbol": token['symbol'],
            "name": token['name'],
            "address": token['address'],
            "description": token['description'],
            "balance": f"{balance:.4f}" if balance > 0 else "N/A"
        }
        print(json.dumps(token_info, indent=2))
    except Exception as e:
        print(f"Error fetching balance for {token['symbol']}: {str(e)}")