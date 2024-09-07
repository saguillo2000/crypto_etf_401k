import os
from dotenv import load_dotenv
from web3 import Account, Web3
from abi import UNISWAP_V3_ROUTER2_ABI, WETH9_ABI, MIN_ERC20_ABI
import eth_abi.packed

load_dotenv()

private_key = os.environ.get("PRIVATE_KEY")

chain_id = 10
rpc_endpoint = "https://opt-mainnet.g.alchemy.com/v2/NC8ECPLoaJ3SxtjqH9AVBli3wAxzWpxr"

web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
account = Account.from_key(private_key)

total_gas_used = 0
amount_in = 1 * 10**13

weth_address = os.environ.get("WETH_ADDRESS")
usdt_address = os.environ.get("USDT_ADDRESS")
swap_router02_address = os.environ.get("SWAP_ROUTER_ADDRESS")

print(f"WETH address: {weth_address}")
print(f"USDT address: {usdt_address}")
print(f"Swap Router address: {swap_router02_address}")

# load contracts
swap_router_contract = web3.eth.contract(address=swap_router02_address, abi=UNISWAP_V3_ROUTER2_ABI)
weth_contract = web3.eth.contract(address=weth_address, abi=WETH9_ABI)
usdt_contract = web3.eth.contract(address=usdt_address, abi=MIN_ERC20_ABI)

print("contract loaded")
# wrap eth
tx = weth_contract.functions.deposit().build_transaction({
        'chainId': web3.eth.chain_id,
        'gas': 50000,
        'gasPrice': int(web3.eth.gas_price * 1.1),
        'nonce': web3.eth.get_transaction_count(account.address),
        'value': amount_in,
})

print("eth wrapped")

signed_transaction = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"tx hash: {Web3.to_hex(tx_hash)}")
total_gas_used += tx_receipt["gasUsed"]

weth_balance = weth_contract.functions.balanceOf(account.address).call()
print(f"weth balance: {weth_balance / 10**18}")
usdt_balance = usdt_contract.functions.balanceOf(account.address).call()
print(f"usdt balance: {usdt_balance / 10**6}")

# Swap ETH for USDT
path = eth_abi.packed.encode_packed(['address','uint24','address'], [weth_address, 500, usdt_address])

tx_params = (
    path, 
    account.address, 
    amount_in,  # amount in
    0  # min amount out (consider adding slippage protection)
)

swap_buy_tx = swap_router_contract.functions.exactInput(tx_params).build_transaction({
    'from': account.address,
    'gas': 300000,
    'maxFeePerGas': web3.eth.gas_price * 2,
    'maxPriorityFeePerGas': web3.eth.max_priority_fee,
    'nonce': web3.eth.get_transaction_count(account.address),
    'value': amount_in,  # Send ETH with the transaction
})

signed_transaction = web3.eth.account.sign_transaction(swap_buy_tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"ETH to USDT swap tx hash: {Web3.to_hex(tx_hash)}")
total_gas_used += tx_receipt["gasUsed"]

weth_balance = weth_contract.functions.balanceOf(account.address).call()
print(f"weth balance: {weth_balance / 10**18}")
usdt_balance = usdt_contract.functions.balanceOf(account.address).call()
print(f"usdt balance: {usdt_balance / 10**6}")
print(f"Total gas used: {total_gas_used}")