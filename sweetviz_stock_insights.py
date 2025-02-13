"""
Stock Data Analysis with Sweetviz

This script fetches historical stock data from Yahoo Finance, analyzes it using Sweetviz,
and generates interactive reports for exploratory data analysis (EDA).

Features:
- Accepts user input for stock tickers and date range.
- Validates input to ensure correct format.
- Generates a general Sweetviz report.
- Compares high vs. low volatility stocks.

Author: Mickias Ambaye
Date: February 2025
"""

import pandas as pd
import numpy as np
import sweetviz as sv
import yfinance as yf
from datetime import datetime

# Set a random seed for reproducibility
np.random.seed(42)


def get_user_input():
    """
    Prompt user for stock tickers and date range, ensuring valid inputs.

    Returns:
    - list: Stock tickers
    - str: Start date (YYYY-MM-DD)
    - str: End date (YYYY-MM-DD)
    """
    while True:
        # Get stock tickers from user
        stocks = input("Enter stock tickers separated by commas (e.g., AAPL,GOOG,MSFT): ").upper().split(",")
        stocks = [s.strip() for s in stocks if s.strip()]  # Remove empty spaces

        if not stocks:
            print("Error: You must enter at least one stock ticker.")
            continue

        # Get start and end dates
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()

        try:
            # Validate date format
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            break  # If everything is valid, break loop
        except ValueError:
            print("Error: Invalid date format. Please enter dates in YYYY-MM-DD format.")

    return stocks, start_date, end_date


def fetch_stock_data(stocks, start, end):
    """
    Fetch historical stock data from Yahoo Finance.

    Parameters:
    stocks (list): List of stock tickers.
    start (str): Start date in YYYY-MM-DD format.
    end (str): End date in YYYY-MM-DD format.

    Returns:
    pd.DataFrame: DataFrame containing Adjusted Close prices.
    """
    try:
        data = yf.download(stocks, start=start, end=end)
        if data.empty:
            print("Error: No data found. Please check stock tickers and date range.")
            return None
        return data['Adj Close'].copy()
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None


def generate_sweetviz_report(df, filename):
    """
    Generate an exploratory data analysis (EDA) report using Sweetviz.

    Parameters:
    df (pd.DataFrame): DataFrame containing stock data.
    filename (str): Output filename for the HTML report.
    """
    report = sv.analyze(df)
    report.show_html(filename)
    print(f"Sweetviz report generated: {filename}")


def generate_volatility_comparison(df, filename):
    """
    Generate a Sweetviz report comparing high vs. low volatility stocks.

    Parameters:
    df (pd.DataFrame): DataFrame containing stock data.
    filename (str): Output filename for the HTML report.
    """
    df['Volatility'] = df.pct_change().std(axis=1)  # Calculate daily volatility
    median_vol = df['Volatility'].median()  # Define threshold
    df['Volatility_Level'] = np.where(df['Volatility'] > median_vol, 'High Volatility', 'Low Volatility')

    report = sv.compare_intra(df, df["Volatility_Level"] == "High Volatility", ["High Volatility", "Low Volatility"])
    report.show_html(filename)
    print(f"Sweetviz volatility comparison report generated: {filename}")


if __name__ == "__main__":
    print("Welcome to the Stock Data Analysis Tool!")

    # Get user input
    stocks, start_date, end_date = get_user_input()

    print("\nFetching stock data...")
    df = fetch_stock_data(stocks, start_date, end_date)

    if df is not None:
        print("\nGenerating general Sweetviz report...")
        generate_sweetviz_report(df, "sweetviz_report.html")

        print("\nGenerating volatility comparison report...")
        generate_volatility_comparison(df, "sweetviz_volatility_report.html")

        print("\nAll reports have been successfully generated.")
    else:
        print("\nFailed to retrieve stock data. Please check your inputs and try again.")
