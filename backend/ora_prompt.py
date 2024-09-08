import os
import json
import time
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider(os.getenv('SEPOLIA_URL_RPC'))) # OP_SEPOLIA_URL_RPC

# Load contract ABI
with open('ora_prompt_abi.json', 'r') as f:
    contract_abi = json.load(f)

# Contract address (replace with your deployed contract address)
contract_address = '0x11d01fa0f5dDf1bd7A75583Bf5CcdA6D8c548efE' # ETH sepolia
#contract_address = '0x1284786a8b79D1D2cd4ca7Cd4DfD8a441B8CE820' # OP sepolia

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Your Ethereum account
account = w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))

def send_transaction(func, *args, **kwargs):
    transaction = func.build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 5000000,
        'gasPrice': int(w3.eth.gas_price * 1.1),
        **kwargs
    })
    signed_txn = account.sign_transaction(transaction)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def estimate_fee():
    return contract.functions.estimateFee().call()

def calculate_ai_result(prompt):
    fee = estimate_fee()
    adjusted_fee = int(fee * 1.2)  # Add 20% buffer
    return send_transaction(contract.functions.calculateAIResult(prompt), value=adjusted_fee)

def get_latest_prompt():
    return contract.functions.getLatestPrompt().call()

def get_latest_response():
    return contract.functions.getLatestResponse().call()

def main():

    prompt = input("Enter your prompt (or 'quit' to exit): ")

    print("Sending prompt to AI Oracle...")
    result = calculate_ai_result(prompt)
    print(f"Transaction hash: {result.transactionHash.hex()}")

    print("Waiting for response...")
    for _ in range(30):  # Wait up to 30 seconds for a response
        time.sleep(1)
        latest_prompt = get_latest_prompt()
        latest_response = get_latest_response()
        if latest_prompt == prompt and latest_response:
            print("Response received:")
            print(latest_response)
            break
    else:
        print("No response received within the timeout period.")

if __name__ == "__main__":
    main()