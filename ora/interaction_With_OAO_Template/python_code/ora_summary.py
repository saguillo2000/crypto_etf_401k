import os
import json
import time
from dotenv import load_dotenv
from web3 import Web3

from wallet_data import get_wallet_data

load_dotenv()

wallet_data = get_wallet_data(os.getenv('PUBLIC_KEY'), os.getenv('OP_MAINNET_URL_RPC'))
print(wallet_data)

# Connect to an Ethereum node (replace with your node URL)
w3 = Web3(Web3.HTTPProvider(os.getenv('SEPOLIA_URL_RPC')))

with open('ora_summary_abi.json', 'r') as f:
    contract_abi = json.load(f)

# Contract address and ABI (you'll need to replace these)
contract_address = '0xce247664E8D0715B0512B6242D1d96e0E3169Ceb'
# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Your Ethereum account (replace with your account details)
account = w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))

# Function to send a transaction
def send_transaction(func, *args, **kwargs):
    transaction = func.build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 5000000,
        'gasPrice': int(w3.eth.gas_price * 1.1),
        **kwargs
    })
    signed_txn = account.sign_transaction(transaction)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

# Example: Call summarizeInvestment function
def summarize_investment(assets):
    fee = contract.functions.estimateFee().call()
    adjusted_fee = int(fee * 1.2)
    # Convert the assets dictionary to a JSON string
    assets_json = json.dumps(assets)
    return send_transaction(contract.functions.summarizeInvestment(assets_json), value=adjusted_fee)

# Example: Get latest prompt
def get_latest_prompt():
    return contract.functions.getLatestPrompt().call()

# Example: Get latest response
def get_latest_response():
    return contract.functions.getLatestResponse().call()

def wait_for_response(max_attempts=60, delay=5):
    print("Waiting for response...")
    initial_prompt = get_latest_prompt()
    for attempt in range(max_attempts):
        time.sleep(delay)
        current_prompt = get_latest_prompt()
        current_response = get_latest_response()
        if current_prompt != initial_prompt and current_response:
            print("Response received:")
            print(current_response)
            return current_response
        print(f"Attempt {attempt + 1}/{max_attempts}. Waiting {delay} seconds...")
    print("No response received within the timeout period.")
    return None

def main():
    print("Summarizing investment...")
    result = summarize_investment(wallet_data)
    print(f"Transaction hash: {result.transactionHash.hex()}")

    response = wait_for_response()
    if response:
        print("--------------------------------")
        print("Investment Summary:")
        print(response)
    else:
        print("Failed to get investment summary. Please try again later.")

if __name__ == "__main__":
    main()