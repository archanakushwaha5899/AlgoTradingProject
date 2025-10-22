import pandas as pd
import os
import matplotlib.pyplot as plt

# ----------- Rule-based Strategy -----------
def apply_trading_strategy(df):
    df['Signal'] = 0  # 0 = Hold, 1 = Buy, -1 = Sell

    # ----- Create crossover conditions
    df.loc[(df['RSI'] < 30) & (df['SMA20'] > df['SMA50']), 'Signal'] = 1  # Buy
    df.loc[(df['RSI'] > 70) | (df['SMA20'] < df['SMA50']), 'Signal'] = -1  # Sell

    # Simulate Positions (carry forward the last signal)
    df['Position'] = df['Signal'].replace(to_replace=0, method='ffill').fillna(0)

    # Calculate daily returns
    df['Return'] = df['Close'].pct_change().fillna(0)
    df['Strategy_Return'] = df['Return'] * df['Position'].shift(1).fillna(0)

    # Cumulative returns
    df['Cumulative_Market_Return'] = (1 + df['Return']).cumprod()
    df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()

    return df

def backtest_all_stocks():
    
    input_dir = "C:/Users/archa/Music/AlgoTradingProject/Processed"
    output_dir = "C:/Users/archa/Music/AlgoTradingProject/Backtest_Results"

    # 🔧 Add this before you list directory
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist!")
        exit()

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path)

            # Ensure required columns exist
            required_cols = ['Close', 'SMA20', 'SMA50', 'RSI']
            if not all(col in df.columns for col in required_cols):
                print(f"Skipping {file} - missing required columns")
                continue

            df = apply_trading_strategy(df)

            # Save backtest results
            output_path = os.path.join(output_dir, file)
            df.to_csv(output_path, index=False)

            # Plot performance
            plt.figure(figsize=(10, 5))
            plt.plot(df['Cumulative_Market_Return'], label='Market Return')
            plt.plot(df['Cumulative_Strategy_Return'], label='Strategy Return')
            plt.title(f"Backtest Result: {file}")
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{file.replace('.csv', '_plot.png')}"))
            plt.close()

            print(f"{file} backtest completed!")

if __name__ == "__main__":
    backtest_all_stocks()
