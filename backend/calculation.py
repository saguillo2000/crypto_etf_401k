
from utils_redstone import get_redstone_price, get_redstone_prices, get_redstone_price_at_yesterday_end
from utils_dbforest import get_connection, get_sqlalchemy_engine, insert_redstone_prices, insert_coingecko_supply
from utils_coingecko import get_coingecko_data
from datetime import datetime, timedelta
import pandas as pd
import json

# logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Connect to the database
conn = get_connection()
alcconn = get_sqlalchemy_engine()

"""
def update_redstone_prices(symbols: list):
    # Get the latest prices for the specified symbols


    prices_dict = get_redstone_prices(symbols)

    # Insert the prices into the database
    if prices_dict:
        insert_redstone_prices(conn, prices_dict)
"""
"""
def update_coingecko_supply(symbols: list):
    # Get the latest supply data for the specified symbols
    for symbol in symbols:
        data = get_coingecko_data(symbol)
        if data:
            # Insert the data into the database
            insert_coingecko_supply(conn, data)
"""

def get_eligible_symbol_list():

    coingecko_list = pd.read_csv('meta/coingecko_metadata.csv')
    redstone_list = pd.read_csv('meta/redstone_metadata.csv')

    redstone_symbols = redstone_list['symbol'].tolist()
    coingecko_symbols = coingecko_list['symbol'].tolist()

    eligible_symbols = list(set(redstone_symbols) & set(coingecko_symbols))

    return eligible_symbols



def get_latest_ciruculating_supply(symbol_list, alcconn):


    #update_circulating_supply(symbol_list)

    df = pd.read_sql('select * from coingecko_supply where date = (select max(date) from coingecko_supply)', alcconn)
    df = df[['symbol', 'circulating_supply']]
    df = df[df['symbol'].isin(symbol_list)]

    circulating_supply_dict = df.set_index('symbol')['circulating_supply'].to_dict()

    return circulating_supply_dict


def get_yesterday_prices_from_db(symbol_list, alcconn):
    # Calculate yesterday's date
    yesterday_date = pd.Timestamp.now().date() - timedelta(days=1)

    # Query the database for prices from yesterday
    query = """
        SELECT symbol, price, date, timestamp
        FROM redstone_price
        WHERE date = %(yesterday_date)s
        AND symbol IN %(symbols)s
    """

    params = {
        'yesterday_date': yesterday_date,
        'symbols': tuple(symbol_list)
    }

    df = pd.read_sql(query, alcconn, params=params)
    prices_dict = df.set_index('symbol')[['price', 'timestamp']].to_dict(orient='index')

    return prices_dict

def get_latest_prices_from_db(symbol_list, alcconn):
    query = """
        SELECT symbol, price, date, timestamp
        FROM redstone_price
        WHERE symbol IN %(symbols)s and date = (select max(date) from redstone_price)
    """

    params = {
        'symbols': tuple(symbol_list)
    }

    df = pd.read_sql(query, alcconn, params=params)
    prices_dict = df.set_index('symbol')[['price', 'timestamp']].to_dict(orient='index')

    return prices_dict


# Function to compute market capitalizations with optimized Redstone API calls

def compute_market_caps_weights(symbol_list, alcconn):
    # Step 1: Get the latest circulating supply from the database
    circulating_supply_dict = get_latest_ciruculating_supply(symbol_list, alcconn)

    # Step 2: Attempt to fetch yesterday's prices from the database
    redstone_prices_db = get_latest_prices_from_db(symbol_list, alcconn)

    # Step 3: Identify symbols missing from the database and fetch them from Redstone
    missing_symbols = [symbol for symbol in symbol_list if symbol.upper() not in redstone_prices_db]
    if missing_symbols:
        logger.warning(f"Fetching prices for missing symbols: {missing_symbols}")

    # Step 4: Create a DataFrame to store the results
    results = []

    for symbol in redstone_prices_db:
        price = redstone_prices_db[symbol]['price']
        circulating_supply = circulating_supply_dict.get(symbol.upper(), None)

        if price and circulating_supply:
            market_cap = price * circulating_supply
            results.append({
                'symbol': symbol,
                'market_cap': market_cap
            })

    # Convert the results to a DataFrame
    market_caps_df = pd.DataFrame(results)

    # Step 5: Compute market cap weights
    total_market_cap = market_caps_df['market_cap'].sum()
    market_caps_df['weight'] = market_caps_df['market_cap'] / total_market_cap

    # Convert the DataFrame to a dictionary with symbol and weight
    market_cap_weights = market_caps_df.set_index('symbol')['weight'].to_dict()

    # Step 6: Return as JSON
    return json.dumps(market_cap_weights, indent=4)




# Example usage:
symbol_list = ['BTC', 'ETH', 'UNI', 'LINK']  # Example list of symbol



# market_caps_df = compute_market_caps_weights(symbol_list, alcconn)
# print(market_caps_df)