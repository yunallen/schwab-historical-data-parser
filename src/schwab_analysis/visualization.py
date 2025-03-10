"""
Visualization module
Functions for creating charts and visualizations of financial data
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from .analysis import generate_summary_statistics

# Set up plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def plot_performance(df, symbol, output_file=None):
    """
    Create a comprehensive visualization of price performance
    
    Args:
        df (pandas.DataFrame): DataFrame with calculated metrics
        symbol (str): Symbol being visualized
        output_file (str, optional): Path to save the plot
    """
    # Generate summary statistics
    summary = generate_summary_statistics(df)
    
    # Create a new figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 14), 
                                        gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # Plot 1: Price with Moving Averages
    ax1.plot(df.index, df['close'], linewidth=2, color='#1f77b4', label='Price')
    ax1.plot(df.index, df['ma_20'], linewidth=1.5, color='#ff7f0e', label='20-Day MA')
    ax1.plot(df.index, df['ma_50'], linewidth=1.5, color='#2ca02c', label='50-Day MA')
    
    # Add Bollinger Bands
    ax1.fill_between(df.index, df['upper_band'], df['lower_band'], 
                     color='#1f77b4', alpha=0.1, label='Bollinger Bands')
    
    ax1.set_title(f'{symbol} Price Performance', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')
    
    # Plot 2: Volume
    volume_scaled = df['volume'] / df['volume'].max() * 100  # Scale for visibility
    ax2.bar(df.index, volume_scaled, color='#1f77b4', alpha=0.5)
    ax2.set_ylabel('Volume (Relative)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: RSI
    ax3.plot(df.index, df['rsi'], color='purple', linewidth=1.5)
    ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5)
    ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5)
    ax3.set_ylabel('RSI', fontsize=14)
    ax3.set_ylim(0, 100)
    ax3.grid(True, alpha=0.3)
    
    # Format dates on x-axis for all subplots
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Add performance metrics as text annotations
    performance_text = (
        f"Period: {summary['start_date']} to {summary['end_date']}\n"
        f"Starting Price: ${summary['start_price']:.2f}\n"
        f"Ending Price: ${summary['end_price']:.2f}\n"
        f"Total Return: {summary['total_return_pct']:.2f}%\n"
        f"Annualized Return: {summary['annualized_return_pct']:.2f}%\n"
        f"Annualized Volatility: {summary['annualized_volatility_pct']:.2f}%\n"
        f"Sharpe Ratio: {summary['sharpe_ratio']:.2f}\n"
        f"Maximum Drawdown: {summary['max_drawdown_pct']:.2f}%"
    )
    
    ax1.annotate(
        performance_text, 
        xy=(0.02, 0.02), 
        xycoords='axes fraction',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8),
        fontsize=11
    )
    
    plt.tight_layout()
    
    # Save the plot if an output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
    
    # Return the figure and axes for potential further customization
    return fig, (ax1, ax2, ax3)

def plot_drawdown_chart(df, symbol, output_file=None):
    """
    Create a visualization focusing on drawdowns
    
    Args:
        df (pandas.DataFrame): DataFrame with calculated metrics
        symbol (str): Symbol being visualized
        output_file (str, optional): Path to save the plot
    """
    # Create a new figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                   gridspec_kw={'height_ratios': [3, 1]})
    
    # Plot 1: Price
    ax1.plot(df.index, df['close'], linewidth=2, color='#1f77b4')
    ax1.set_title(f'{symbol} Price and Drawdown Analysis', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Drawdown
    ax2.fill_between(df.index, 0, df['drawdown'], color='red', alpha=0.3)
    ax2.plot(df.index, df['drawdown'], color='red', linewidth=1)
    ax2.set_ylabel('Drawdown (%)', fontsize=14)
    ax2.set_ylim(df['drawdown'].min() * 1.1, 5)  # Set y-axis to show drawdowns plus some padding
    ax2.grid(True, alpha=0.3)
    
    # Format dates on x-axis for all subplots
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Find and annotate major drawdowns (below -10%)
    major_drawdowns = df[df['drawdown'] < -10]
    
    if not major_drawdowns.empty:
        # Group consecutive drawdown days
        drawdown_events = []
        current_event = []
        
        for idx, row in major_drawdowns.iterrows():
            if not current_event or (idx - current_event[-1].name).days <= 30:  # Consider drawdowns within 30 days part of same event
                current_event.append(row)
            else:
                drawdown_events.append(current_event)
                current_event = [row]
        
        if current_event:
            drawdown_events.append(current_event)
        
        # Annotate the worst point of each major drawdown event
        for event in drawdown_events:
            event_df = pd.DataFrame(event)
            worst_day = event_df.loc[event_df['drawdown'].idxmin()]
            date = worst_day.name.strftime('%Y-%m-%d')
            drawdown_value = worst_day['drawdown']
            
            ax2.annotate(
                f"{date}: {drawdown_value:.1f}%",
                xy=(worst_day.name, drawdown_value),
                xytext=(10, -30),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="black"),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8),
                fontsize=9
            )
    
    plt.tight_layout()
    
    # Save the plot if an output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
    
    # Return the figure and axes for potential further customization
    return fig, (ax1, ax2)