import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Connect to an Ethereum node (replace with your node URL)
w3 = Web3(Web3.HTTPProvider(os.getenv('RPC_URL')))

with open('Summary_abi.json', 'r') as f:
    contract_abi = json.load(f)

# Contract address and ABI (you'll need to replace these)
#contract_address = '0x2b5a4aE5490834a5F232fD00AE54BbF90425EF94'
contract_address = '0xdE42b37719156BD7d648C11EC3732eb748A9deC4'
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
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

# Example: Call summarizeInvestment function
def summarize_investment(assets):
    fee = contract.functions.estimateFee().call()
    adjusted_fee = int(fee * 1.2)
    return send_transaction(contract.functions.summarizeInvestment(assets), value=adjusted_fee)

# Example: Get latest prompt
def get_latest_prompt():
    return contract.functions.getLatestPrompt().call()

# Example: Get latest response
def get_latest_response():
    return contract.functions.getLatestResponse().call()

assets = [
    ("BTC", "Bitcoin is the first decentralized cryptocurrency, created in 2009 by an anonymous person or group known as Satoshi Nakamoto. It operates on a peer-to-peer network, allowing users to send and receive payments without the need for intermediaries like banks. Bitcoin's underlying technology, the blockchain, ensures transparency and security by recording all transactions in a public ledger. It is widely recognized as a store of value and a medium of exchange.", 65),
    ("ETH", "Ethereum is a decentralized, open-source blockchain platform that enables the creation and execution of smart contracts and decentralized applications (dApps). It was proposed by Vitalik Buterin in 2013 and launched in 2015. Ethereum's native cryptocurrency, Ether (ETH), is used to power transactions and computational services on the network. The platform is known for its flexibility, allowing developers to build and deploy a wide range of applications beyond just cryptocurrency.", 20),
    ("BNB", "BNB (Binance Coin) is the native cryptocurrency of the Binance ecosystem, initially launched as an ERC-20 token on the Ethereum blockchain in 2017. It was later migrated to Binance's own blockchain, Binance Chain. BNB is used primarily to pay for transaction fees on the Binance exchange, participate in token sales, and other services within the Binance ecosystem. Over time, BNB has gained broader utility, including in decentralized finance (DeFi) applications and as a payment method across various platforms.", 10),
    ("SOL", "Solana is a high-performance blockchain platform designed for scalable decentralized applications (dApps) and cryptocurrencies. Launched in 2020, it uses a unique consensus mechanism called Proof of History (PoH) combined with Proof of Stake (PoS) to achieve fast transaction speeds and low costs. Solana's native cryptocurrency, SOL, is used to pay for transaction fees, staking, and participating in the network's governance. SOL has become popular for its role in supporting a growing ecosystem of DeFi projects, NFTs, and other blockchain-based applications.", 5)
]
# result = summarize_investment(assets)
# print(f"Transaction hash: {result.transactionHash.hex()}")

latest_prompt = get_latest_prompt()
latest_response = get_latest_response()

print("--------------------------------")
print("Prompt:")
print(f"Latest prompt: {latest_prompt}")
print("--------------------------------")
print("Response:")
print(f"Latest response: {latest_response}")