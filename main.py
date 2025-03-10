#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Schwab API SPY Analysis
Main script that coordinates the analysis workflow
"""

import os
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import project modules
from src.schwab_analysis.auth import load_credentials, initialize_client
from src.schwab_analysis.data import get_historical_data
from src.schwab_analysis.analysis import calculate_metrics
from src.schwab_analysis.visualization import plot_performance

# Ensure output directories exist
os.makedirs("output/data", exist_ok=True)
os.makedirs("output/charts", exist_ok=True)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analyze SPY historical data using Schwab API")
    
    parser.add_argument(
        "--symbol", 
        type=str, 
        default="SPY",
        help="Symbol to analyze (default: SPY)"
    )
    
    parser.add_argument(
        "--days", 
        type=int, 
        default=365,
        help="Number of days of historical data to retrieve (default: 365)"
    )
    
    parser.add_argument(
        "--output-data", 
        type=str, 
        default="output/data/spy_historical_data.csv",
        help="Path to save data CSV (default: output/data/spy_historical_data.csv)"
    )
    
    parser.add_argument(
        "--output-chart", 
        type=str, 
        default="output/charts/spy_performance.png",
        help="Path to save chart (default: output/charts/spy_performance.png)"
    )
    
    return parser.parse_args()

def main():
    """Main function to execute the analysis workflow"""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Set date range for historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=args.days)
        
        print(f"Analyzing {args.symbol} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        
        # Step 1: Load API credentials and initialize client
        credentials = load_credentials()
        client = initialize_client(credentials)
        
        # Step 2: Retrieve historical data
        print(f"Retrieving historical data for {args.symbol}...")
        raw_data = get_historical_data(client, args.symbol, start_date, end_date)
        
        # Step 3: Calculate performance metrics
        print("Calculating performance metrics...")
        enhanced_data = calculate_metrics(raw_data)
        
        # Step 4: Generate visualization
        print("Generating performance visualization...")
        plot_performance(enhanced_data, args.symbol, output_file=args.output_chart)
        
        # Step 5: Save data to CSV
        enhanced_data.to_csv(args.output_data)
        print(f"Data saved to {args.output_data}")
        
        print(f"Analysis complete! Chart saved to {args.output_chart}")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()