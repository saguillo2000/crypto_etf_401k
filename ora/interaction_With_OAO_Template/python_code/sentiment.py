import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sentiment(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis expert. Analyze the given text and respond with only 'positive' or 'negative'."},
            {"role": "user", "content": f"Analyze the sentiment of the following text: '{text}'"}
        ],
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    sentiment = response.choices[0].message.content.strip().lower()
    return "Keep" if sentiment == "positive" else "Sell"

def get_investment_decision(asset_description):
    decision = analyze_sentiment(asset_description)
    print(f"Asset description: {asset_description}")
    print(f"Investment decision: {decision}")
    print()

# Example usage
assets = [
    "Bitcoin has shown strong growth and adoption in recent months, with major institutions investing heavily.",
    "Ethereum's recent network upgrade has faced delays and technical issues, causing concern among investors.",
    "The new cryptocurrency project has been accused of being a scam, with many early investors reporting losses.",
    "The blockchain platform has secured partnerships with major tech companies, signaling potential for widespread adoption."
]

for asset in assets:
    get_investment_decision(asset)