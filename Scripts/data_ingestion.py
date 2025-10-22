import yfinance as yf
import pandas as pd
import os

# Ensure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Choose 3 NIFTY50 STOCKS
stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

for stock in stocks:
    df = yf.download(stock, period='6mo', interval='1d')
    if df.empty:
        print(f"No Data Found for {stock}, Skipping...")
        continue

    # Basics to EDA
    print("--------{stock}-----------")

    # Save to CSV File
    df.to_csv(f'data/{stock.replace(".","_")}_6mo.csv')
    print(stock, 'saved successfully!')

