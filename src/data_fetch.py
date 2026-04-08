import yfinance as yf
import pandas as pd
import os

def fetch_and_save(ticker):
    df = yf.Ticker(ticker).history(period="6mo", interval="1d")
    df.reset_index(inplace=True)

    path = r"C:\Users\archa\Videos\Project\AlgoTradingProject\data"
    os.makedirs(path, exist_ok=True)

    file_name = ticker.replace(".NS", "").lower() + ".csv"
    df.to_csv(f"{path}\\{file_name}", index=False)

    print(f"{ticker} data saved!")

# Stocks list
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]

for stock in stocks:
    fetch_and_save(stock)