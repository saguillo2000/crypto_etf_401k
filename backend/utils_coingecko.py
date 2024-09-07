import pandas as pd
import requests
import os
import csv

api_key = os.getenv("COINGECKO_APIKEY")


def create_coingecko_metadata():
    def fetch_all_coins():
        # Define the endpoint URL
        url = "https://api.coingecko.com/api/v3/coins/list"

        # Make the request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def save_to_csv(data, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the headers
            writer.writerow(['coingecko_id', 'symbol', 'name'])

            # Write the data
            for coin in data:
                writer.writerow([coin['id'], coin['symbol'].upper(), coin['name']])

    # Fetch all coins data
    coins_data = fetch_all_coins()

    # Save to CSV
    if coins_data:
        save_to_csv(coins_data, 'coingecko_coin_list.csv')
        print(f"Saved {len(coins_data)} coins to CSV.")


def get_coingecko_data(asset_id):
    # Define the endpoint URL
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # Set query parameters
    params = {
        'vs_currency': 'usd',  # Currency (USD)
        'ids': asset_id  # Coin ID (e.g., 'bitcoin')
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        data_dict = {}
        if data:
            symbol = data[0]['symbol']
            data_dict[symbol] = {
                'market_cap': data[0]['market_cap'],
                'circulating_supply': data[0]['circulating_supply'],
                'total_supply': data[0]['total_supply'],
                'current_price': data[0]['current_price'],
                'last_updated': data[0]['last_updated']
            }
        return data_dict
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def coingecko_symbol_mapper(symbol_list: list):
    coingecko_df = pd.read_csv('meta/coingecko_metadata.csv')
    coingecko_df = coingecko_df[coingecko_df['symbol'].isin(symbol_list)]
    return coingecko_df[['symbol', 'coingecko_id']]





# Example usage

if __name__== '__main__':
    data = get_coingecko_data('bitcoin')
    print(data)

