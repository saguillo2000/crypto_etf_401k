from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
from sqlalchemy import create_engine
from utils_dbforest import get_sqlalchemy_engine  # Assuming this is in your utils_dbforest.py
from calculation import compute_market_caps_weights

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