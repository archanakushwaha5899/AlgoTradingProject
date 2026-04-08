import yfinance as yf
import pandas as pd
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


# Google Sheets Connection
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
creds_path = os.path.join(BASE_DIR, "credentials.json")

creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)

client = gspread.authorize(creds)
sheet = client.open("AlgoTradingLogs").sheet1

# Stocks
stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",
    "HINDUNILVR.NS", "ITC.NS", "LT.NS", "KOTAKBANK.NS"
]

for stock in stocks:

    df = yf.download(stock, start="2020-01-01", end="2024-01-01", progress=False)
    df = df.reset_index()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df['Date'] = pd.to_datetime(df['Date'])

    # Indicators
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()

    # Signal
    df['Signal'] = "HOLD"
    df.loc[df['SMA_20'] > df['SMA_50'], 'Signal'] = "BUY"
    df.loc[df['SMA_20'] < df['SMA_50'], 'Signal'] = "SELL"

    latest = df.iloc[-1]

    date = str(latest['Date'])[:10]
    price = round(float(latest['Close']), 2)
    signal = latest['Signal']
    stock_name = stock.replace(".NS", "")

    # Logging
    quantity = 10

    data = sheet.get_all_values()
    rows = data[1:]

    new_entry = [str(date), stock_name, signal, str(price)]
    rows_clean = [[str(col).strip() for col in row[:4]] for row in rows]

    if new_entry in rows_clean:
        print(f"{stock_name}: Duplicate — skipped")
    else:
        if signal == "BUY":
            sheet.append_row([date, stock_name, signal, price, quantity, ""])
            print(f"{stock_name}: BUY logged")

        elif signal == "SELL":
            buy_price = None

            for row in reversed(rows):
                if row[1] == stock_name and row[2] == "BUY":
                    buy_price = float(row[3])
                    break

            pnl = (price - buy_price) * quantity if buy_price else 0

            sheet.append_row([date, stock_name, signal, price, quantity, pnl])
            print(f"{stock_name}: SELL logged with PnL = {pnl}")