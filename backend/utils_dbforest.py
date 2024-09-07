import pandas as pd
import os
import psycopg2
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime, timedelta

from utils_redstone import get_redstone_price, get_redstone_prices, get_redstone_price_at_yesterday_end
from utils_coingecko import get_coingecko_data, coingecko_symbol_mapper


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection():
    connection_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    conn = psycopg2.connect(**connection_params)
    return conn

# Function to get SQLAlchemy engine using environment variables
def get_sqlalchemy_engine():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    return engine

"""
SETUP FUNCTIONS
"""

def get_table_list():
    conn, cursor = get_connection()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()
    return tables

def create_historical_data_table():

    conn, cursor = get_connection()
    # Create the financial_data table
    create_table_query = """
    CREATE TABLE historical_data (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        symbol VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        market_cap NUMERIC,
        volume NUMERIC,
        price NUMERIC
    );
    """
    cursor.execute(create_table_query)
    conn.commit()  # Apply changes

def create_coingecko_supply_table():
    conn = get_connection()
    cursor = conn.cursor()
    # Create the financial_data table
    create_table_query = """
    CREATE TABLE coingecko_supply (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        symbol VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        circulating_supply NUMERIC,
        total_supply NUMERIC,
        current_price NUMERIC,
        last_updated TIMESTAMPTZ
    );
    """
    cursor.execute(create_table_query)
    conn.commit()  # Apply changes

def create_redstone_price_table():
    conn = get_connection()
    cursor = conn.cursor()
    # Create the redstone_price table with a date field
    create_table_query = """
    CREATE TABLE redstone_price (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        symbol VARCHAR(10) NOT NULL,
        price NUMERIC,
        date DATE NOT NULL,  -- New date field
        timestamp TIMESTAMPTZ
    );
    """
    cursor.execute(create_table_query)
    conn.commit()  # Apply changes


"""
READ AND WRITE FUNCTIONS
"""

def insert_redstone_prices(conn, prices_dict):
    cursor = conn.cursor()

    try:
        # Insert query
        insert_query = """
        INSERT INTO redstone_price (symbol, price, date, timestamp)
        VALUES (%s, %s, %s, to_timestamp(%s))
        """

        # Loop through the prices dictionary and insert values
        for symbol, data in prices_dict.items():
            # Convert the timestamp to seconds (from pandas datetime)
            timestamp_sec = int(data['timestamp'].timestamp())
            # Extract the date from the timestamp (date part only)
            date = data['timestamp'].date()

            # Execute the insert query with symbol, price, date, and timestamp
            cursor.execute(insert_query, (symbol, data['value'], date, timestamp_sec))

        # Commit the changes
        conn.commit()
        logging.info(f"Inserted {len(prices_dict)} rows successfully.")

    except Exception as e:
        logging.error(f"Error while inserting data: {e}")

    finally:
        cursor.close()  # Only close the cursor, not the connection

def insert_coingecko_supply(conn, data_dict):
    cursor = conn.cursor()

    try:
        # Insert query
        insert_query = """
        INSERT INTO coingecko_supply (symbol, date, circulating_supply, total_supply, current_price, last_updated)
        VALUES (%s, %s, %s, %s, %s, to_timestamp(%s, 'YYYY-MM-DD"T"HH24:MI:SSZ'))
        """

        # Loop through the data dictionary and insert values
        for symbol, data in data_dict.items():
            date = pd.to_datetime(data['last_updated']).date()  # Extract the date part
            cursor.execute(insert_query, (
                symbol.upper(),
                date,
                data['circulating_supply'],
                data['total_supply'],
                data['current_price'],
                data['last_updated']
            ))

        # Commit the changes
        conn.commit()
        logger.info(f"Inserted data for {len(data_dict)} assets successfully.")
    except Exception as e:
        logger.error(f"Error while inserting data: {e}")

    finally:
        cursor.close()

# Function to insert multiple rows from a DataFrame
def insert_historical_data(df, conn):
    try:
        # Use the passed connection to get the cursor
        cursor = conn.cursor()

        # Insert query
        insert_query = """
        INSERT INTO financial_data (symbol, market_cap, volume, price, date)
        VALUES (%s, %s, %s, %s, %s);
        """

        # Convert DataFrame rows to a list of tuples
        data = list(df.itertuples(index=False, name=None))

        # Execute the insert query for all rows at once
        cursor.executemany(insert_query, data)

        # Commit the transaction
        conn.commit()

        print(f"{len(data)} rows inserted successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while inserting data: {error}")

    finally:
        # No need to close the connection here
        cursor.close()  # We only close the cursor

def update_circulating_supply(conn, managed_symbols):
    coingecko_map = coingecko_symbol_mapper(managed_symbols)
    df = pd.read_sql('select * from coingecko_supply', conn)
    df = df[['symbol', 'date', 'circulating_supply']]
    today_date = pd.Timestamp.now().date()
    # select df where date == today_date
    df = df[df['date'] == today_date]

    # for each symbol not in df, get the latest data from coingecko and insert it into the db
    for symbol in managed_symbols:
        if symbol not in df['symbol'].tolist():
            # add a mapper
            coingecko_id = coingecko_map[coingecko_map['symbol'] == symbol]['coingecko_id'].values[0]
            data = get_coingecko_data(coingecko_id)
            if data:
                insert_coingecko_supply(conn, data)
                print(f"Inserted data for {symbol} successfully.")
            else:
                print(f"Failed to insert data for {symbol}.")

def update_redstone_prices(conn, managed_symbols):
    # Calculate yesterday's date
    yesterday_date = pd.Timestamp.now().date() - timedelta(days=1)

    # Query the database to get already downloaded prices for yesterday
    df = pd.read_sql('SELECT symbol, date FROM redstone_price', conn)
    df = df[['symbol', 'date']]

    # Filter for yesterday's date
    df_yesterday = df[df['date'] == yesterday_date]

    # Fetch prices from Redstone for the symbols not in yesterday's data
    missing_symbols = [symbol for symbol in managed_symbols if symbol not in df_yesterday['symbol'].tolist()]

    if missing_symbols:
        # Fetch and insert data for missing symbols
        logger.info(f"Fetching prices for missing symbols: {missing_symbols}")
        prices_dict = get_redstone_price_at_yesterday_end(missing_symbols)
        if prices_dict:
            insert_redstone_prices(conn, prices_dict)
            logger.info(f"Inserted prices for symbols: {missing_symbols}")
        else:
            logger.error(f"Failed to fetch prices for {missing_symbols}")
    else:
        logger.info("All prices already downloaded for yesterday.")


def insert_historical_data(conn, ):
    df = pd.read_csv('hist_data_latest.csv')

    df = pd.read_csv('hist_data_latest.csv')

    symbol_list = ['BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'DOGE', 'DOT', 'UNI', 'LTC', 'LINK']
    symbol_list = ['BTC']
    df = df[df['symbol'].isin(symbol_list)]
    # Prepare a cursor for database operations
    cursor = conn.cursor()

    try:
        # Insert query
        insert_query = """
            INSERT INTO historical_data (symbol, date, market_cap, volume, price)
            VALUES (%s, %s, %s, %s, %s)
            """

        # Loop through the DataFrame and insert values into the table
        for index, row in df.iterrows():
            # Ensure the date format is correct if needed (e.g., converting to string if necessary)
            date = pd.to_datetime(row['date']).date()

            # Execute the insert query with the appropriate data
            cursor.execute(insert_query, (
                row['symbol'],
                date,
                row['market_cap'],
                row['volume'],
                row['price']
            ))

        # Commit the changes to the database
        conn.commit()
        logging.info(f"Inserted {len(df)} rows successfully into historical_data table.")

    except Exception as e:
        # Handle any errors during the insertion process
        logging.error(f"Error while inserting historical data: {e}")
        conn.rollback()  # Rollback in case of an error

    finally:
        cursor.close()  # Close the cursor

conn = get_connection()
insert_historical_data(conn)

#create_redstone_price_table()
#create_historical_data_table()
#print(get_table_list())