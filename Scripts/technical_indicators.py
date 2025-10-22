import pandas as pd
import os

# Function to calculate indicators
def calculate_indicators(df):
    # Convert columns to numeric
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')

    # --- RSI (14) ---
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # --- Simple Moving Averages ---
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()

    # --- MACD (12-26) ---
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df


# Function to process all stock CSVs
def process_all_stocks():
    input_dir = "C:/Users/archa/Music/AlgoTradingProject/Data"
    output_dir = "C:/Users/archa/Music/AlgoTradingProject/Processed"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path)
            df = calculate_indicators(df)
            output_path = os.path.join(output_dir, file)
            df.to_csv(output_path, index=False)
            print(f"{file} processed successfully!")

if __name__ == "__main__":
    process_all_stocks()
