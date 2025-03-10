"""
Data analysis module
Contains functions for calculating financial metrics and analyzing performance
"""

import pandas as pd
import numpy as np

def calculate_metrics(df):
    """
    Calculate additional performance metrics for the price data
    
    Args:
        df (pandas.DataFrame): DataFrame containing historical price data
        
    Returns:
        pandas.DataFrame: DataFrame with additional metrics added
    """
    # Create a copy of the DataFrame
    result = df.copy()
    
    # Calculate daily returns
    result['daily_return'] = result['close'].pct_change() * 100
    
    # Calculate cumulative returns
    result['cumulative_return'] = (1 + result['daily_return'] / 100).cumprod() - 1
    result['cumulative_return_pct'] = result['cumulative_return'] * 100
    
    # Calculate moving averages
    result['ma_20'] = result['close'].rolling(window=20).mean()
    result['ma_50'] = result['close'].rolling(window=50).mean()
    result['ma_200'] = result['close'].rolling(window=200).mean()
    
    # Calculate volatility (20-day standard deviation of returns)
    result['volatility'] = result['daily_return'].rolling(window=20).std()
    
    # Calculate Bollinger Bands
    result['upper_band'] = result['ma_20'] + (result['volatility'] * 2 / 100 * result['ma_20'])
    result['lower_band'] = result['ma_20'] - (result['volatility'] * 2 / 100 * result['ma_20'])
    
    # Calculate drawdowns
    result['peak'] = result['close'].cummax()
    result['drawdown'] = (result['close'] / result['peak'] - 1) * 100
    
    # Calculate relative strength index (RSI)
    delta = result['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    rs = avg_gain / avg_loss
    result['rsi'] = 100 - (100 / (1 + rs))
    
    return result

def generate_summary_statistics(df):
    """
    Generate summary statistics from the enhanced data
    
    Args:
        df (pandas.DataFrame): DataFrame with calculated metrics
        
    Returns:
        dict: Dictionary containing summary statistics
    """
    # Extract start and end dates
    start_date = df.index[0].strftime('%Y-%m-%d')
    end_date = df.index[-1].strftime('%Y-%m-%d')
    
    # Calculate basic performance metrics
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    total_return = (end_price / start_price - 1) * 100
    
    # Calculate annualized return
    days = (df.index[-1] - df.index[0]).days
    annualized_return = ((1 + total_return / 100) ** (365 / days) - 1) * 100
    
    # Calculate volatility metrics
    daily_volatility = df['daily_return'].std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    # Calculate Sharpe ratio (assuming risk-free rate of 2%)
    risk_free_rate = 2.0
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    
    # Calculate maximum drawdown
    max_drawdown = df['drawdown'].min()
    
    # Calculate best and worst days
    best_day = df['daily_return'].max()
    best_day_date = df.loc[df['daily_return'].idxmax()].name.strftime('%Y-%m-%d')
    worst_day = df['daily_return'].min()
    worst_day_date = df.loc[df['daily_return'].idxmin()].name.strftime('%Y-%m-%d')
    
    # Calculate percentage of positive days
    positive_days_pct = (df['daily_return'] > 0).mean() * 100
    
    # Compile the summary statistics
    summary = {
        'start_date': start_date,
        'end_date': end_date,
        'start_price': start_price,
        'end_price': end_price,
        'total_return_pct': total_return,
        'annualized_return_pct': annualized_return,
        'daily_volatility_pct': daily_volatility,
        'annualized_volatility_pct': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown_pct': max_drawdown,
        'best_day_pct': best_day,
        'best_day_date': best_day_date,
        'worst_day_pct': worst_day,
        'worst_day_date': worst_day_date,
        'positive_days_pct': positive_days_pct
    }
    
    return summary