from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
from sqlalchemy import create_engine
from utils_dbforest import get_sqlalchemy_engine  # Assuming this is in your utils_dbforest.py
from calculation import compute_market_caps_weights
import os
from dotenv import load_dotenv
import time

from wallet_data import get_wallet_data
from ora_summary import summarize_investment, wait_for_response
from ora_prompt import calculate_ai_result, get_latest_prompt, get_latest_response

load_dotenv()

# Initialize FastAPI app
app = FastAPI()
engine = get_sqlalchemy_engine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Input model
class MarketCapRequest(BaseModel):
    symbols: list[str]


# Endpoint to compute market cap weights
@app.post("/compute_market_caps_weights/")
def compute_market_caps(request: MarketCapRequest):
    # Establish connection to the database
    try:
        weights = compute_market_caps_weights(request.symbols, engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing market cap weights: {str(e)}")

    return json.loads(weights)  # Return the weights as JSON

# Endpoint to compute market cap weights
@app.post("/gen_wallet_summary/")
def wallet_summary():
    wallet_data = get_wallet_data(os.getenv('PUBLIC_KEY'), os.getenv('OP_MAINNET_URL_RPC'))
    print("Summarizing investment...")
    result = summarize_investment(wallet_data)
    print(f"Transaction hash: {result.transactionHash.hex()}")

    response = wait_for_response()
    return response

class PromptRequest(BaseModel):
    prompt: str

@app.post("/gen_prompt/")
def gen_prompt(request: PromptRequest):
    prompt = request.prompt

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

    return latest_response