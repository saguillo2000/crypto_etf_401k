import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assets = [
    ("BTC", "Bitcoin is the first decentralized cryptocurrency, created in 2009 by an anonymous person or group known as Satoshi Nakamoto. It operates on a peer-to-peer network, allowing users to send and receive payments without the need for intermediaries like banks. Bitcoin's underlying technology, the blockchain, ensures transparency and security by recording all transactions in a public ledger. It is widely recognized as a store of value and a medium of exchange.", 65),
    ("ETH", "Ethereum is a decentralized, open-source blockchain platform that enables the creation and execution of smart contracts and decentralized applications (dApps). It was proposed by Vitalik Buterin in 2013 and launched in 2015. Ethereum's native cryptocurrency, Ether (ETH), is used to power transactions and computational services on the network. The platform is known for its flexibility, allowing developers to build and deploy a wide range of applications beyond just cryptocurrency.", 20),
    ("BNB", "BNB (Binance Coin) is the native cryptocurrency of the Binance ecosystem, initially launched as an ERC-20 token on the Ethereum blockchain in 2017. It was later migrated to Binance's own blockchain, Binance Chain. BNB is used primarily to pay for transaction fees on the Binance exchange, participate in token sales, and other services within the Binance ecosystem. Over time, BNB has gained broader utility, including in decentralized finance (DeFi) applications and as a payment method across various platforms.", 10),
    ("SOL", "Solana is a high-performance blockchain platform designed for scalable decentralized applications (dApps) and cryptocurrencies. Launched in 2020, it uses a unique consensus mechanism called Proof of History (PoH) combined with Proof of Stake (PoS) to achieve fast transaction speeds and low costs. Solana's native cryptocurrency, SOL, is used to pay for transaction fees, staking, and participating in the network's governance. SOL has become popular for its role in supporting a growing ecosystem of DeFi projects, NFTs, and other blockchain-based applications.", 5)
]

def create_prompt(assets):
    prompt = "Analyze and explain the following investment cryptocurrency portfolio. This only focuses on crypto assets:\n\n"
    for i, (token, description, distribution) in enumerate(assets, 1):
        prompt += f"Asset {i}: {description} ({distribution}% of portfolio)\n"
        prompt += f"Token Name: {token}\n\n"
    
    prompt += """Please provide a comprehensive explanation of these assets and their distribution in the investment portfolio. 
Consider the following points in your analysis:
1. Brief description of each asset and its key characteristics
2. Rationale behind the distribution percentages based on market cap
3. Potential risks and benefits of this portfolio composition
4. How this distribution might reflect current market trends or investor sentiment
5. Any notable synergies or diversification benefits among the assets
6. The significance of the specific tokens chosen for each asset category

Provide your analysis in a clear, concise manner suitable for both novice and experienced investors."""
    
    return prompt

def get_summary_analysis(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable cryptocurrency analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].message.content.strip()

# Create the prompt
prompt = create_prompt(assets)

# Get the summary analysis
summary = get_summary_analysis(prompt)

print("Investment Portfolio Analysis:")
print(summary)