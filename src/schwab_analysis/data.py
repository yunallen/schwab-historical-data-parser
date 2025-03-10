"""
Data retrieval module for Schwab API
Handles fetching historical price data
"""

import pandas as pd
from datetime import datetime

def get_historical_data(client, symbol, start_date, end_date):
    """
    Retrieve historical price data for a given symbol
    
    Args:
        client (schwab.client.Client): Authenticated Schwab client
        symbol (str): Stock/ETF symbol to retrieve data for
        start_date (str): Start date for historical data (YYYY-MM-DD)
        end_date (str): End date for historical data (YYYY-MM-DD)
        
    Returns:
        pandas.DataFrame: DataFrame containing historical price data
    """
    try:
        # Convert string dates to datetime objects if provided as strings
        start_date_obj = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, '%Y-%m-%d')

        # Get historical price data using the client
        # The actual method name and parameters may vary based on the library implementation
        response = client.get_price_history(
            symbol=symbol,
            start_datetime=start_date_obj,
            end_datetime=end_date_obj,
            period_type=client.PriceHistory.PeriodType.YEAR,
            frequency_type=client.PriceHistory.FrequencyType.DAILY,
            frequency=client.PriceHistory.Frequency.DAILY
        )
        
        # Process the response into a pandas DataFrame
        candles = response.json()['candles']
        df = pd.DataFrame(candles)
        
        # Process the data
        # Convert timestamp to datetime
        df['date'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('date', inplace=True)
        
        # Drop the original datetime column
        if 'datetime' in df.columns:
            df.drop('datetime', axis=1, inplace=True)
            
        return df
    
    except Exception as e:
        print(f"Exception when retrieving historical data: {e}")
        raise

def get_quote(client, symbol):
    """
    Get current quote information for a symbol
    
    Args:
        client (schwab.client.Client): Authenticated Schwab client
        symbol (str): Stock/ETF symbol to retrieve quote for
        
    Returns:
        dict: Quote information
    """
    try:
        # Get quote data using the client
        response = client.get_quote(symbol)
        
        # Return the quote data
        return response.json()
    
    except Exception as e:
        print(f"Exception when getting quote: {e}")
        raise