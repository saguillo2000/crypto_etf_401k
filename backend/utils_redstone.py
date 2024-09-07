import requests
import pandas as pd
from datetime import datetime, timedelta

import requests

def get_redstone_price(symbol):
    # Define the base URL for the Redstone API
    base_url = "https://api.redstone.finance/prices"

    # Make the request to get the latest price for the specified symbol
    response = requests.get(f"{base_url}?symbol={symbol}&provider=redstone")

    # Check if the request was successful
    if response.status_code == 200:
        price_data = response.json()[0]  # Get the first (and only) result in the response
        price_dict = {
            'price': price_data['value'],  # Map 'value' to 'price'
            'timestamp': price_data['timestamp']  # Keep the 'timestamp'
        }

        return price_dict
    else:
        return None


def get_redstone_prices(symbols):
    base_url = "https://api.redstone.finance/prices"

    # Convert the list of symbols to a comma-separated string
    symbols = [symbol.upper() for symbol in symbols]
    symbols_str = ",".join(symbols)

    # Make the request to get the latest prices for the specified symbols
    response = requests.get(f"{base_url}?symbols={symbols_str}&provider=redstone")

    # Check if the request was successful
    if response.status_code == 200:
        prices_data = response.json()
        prices_dict = {}

        # Loop through the symbols in the response data
        for symbol in prices_data:
            # Convert the timestamp to datetime (from ms)
            timestamp = pd.to_datetime(prices_data[symbol]['timestamp'], unit='ms')
            prices_dict[symbol] = {
                'value': prices_data[symbol]['value'],
                'timestamp': timestamp
            }
        return prices_dict
    else:
        return None


def get_redstone_price_at_yesterday_end(symbols):
    base_url = "https://api.redstone.finance/prices"

    # Calculate yesterday's end of the day (23:59) in milliseconds
    yesterday_end = datetime.combine(datetime.now() - timedelta(1), datetime.max.time())
    timestamp = int(yesterday_end.timestamp() * 1000)  # Convert to milliseconds

    prices_dict = {}

    for symbol in symbols:
        # Prepare query parameters
        params = {
            'symbol': symbol.upper(),
            'provider': 'redstone',
            'toTimestamp': timestamp,
            'limit': 1  # Only fetch 1 price closest to that timestamp
        }

        # Make the request
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            prices_data = response.json()

            if len(prices_data) > 0:
                # Convert the timestamp to datetime (from ms)
                timestamp_dt = pd.to_datetime(prices_data[0]['timestamp'], unit='ms')
                prices_dict[symbol.upper()] = {
                    'value': prices_data[0]['value'],
                    'timestamp': timestamp_dt
                }
            else:
                print(f"No price data returned for {symbol}.")
        else:
            print(f"Error for {symbol}: {response.status_code}, {response.text}")

    return prices_dict if prices_dict else None

# Example usage


if __name__ =='__main__':
    pass

