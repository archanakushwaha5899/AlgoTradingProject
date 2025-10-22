import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths
RULE_DIR = "C:/Users/archa/Music/AlgoTradingProject/Backtest_Results"
ML_DIR = "C:/Users/archa/Music/AlgoTradingProject/ML_Results"
OUTPUT_DIR = "C:/Users/archa/Music/AlgoTradingProject/Comparison_Results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

summary = []

# List all stocks based on rule-based CSVs
for file in os.listdir(RULE_DIR):
    if file.endswith(".csv"):
        stock_name = file.replace('.csv', '')
        rule_path = os.path.join(RULE_DIR, file)
        ml_path = os.path.join(ML_DIR, file)

        # Load rule-based results
        rule_df = pd.read_csv(rule_path)
        rule_return = rule_df['Cumulative_Strategy_Return'].iloc[-1]

        # Load ML results if available
        if os.path.exists(ml_path):
            ml_df = pd.read_csv(ml_path)
            if 'Predicted' in ml_df.columns:
                ml_signals = ml_df['Predicted'].fillna(0)
                ml_return = (ml_df['Close'].pct_change().fillna(0) * ml_signals.shift(1).fillna(0) + 1).cumprod().iloc[-1]
            else:
                ml_return = None
        else:
            ml_return = None

        summary.append({
            'Stock': stock_name,
            'Rule_Based_Return': rule_return,
            'ML_Strategy_Return': ml_return
        })

        # Plot comparison
        plt.figure(figsize=(10,5))
        plt.plot(rule_df['Cumulative_Strategy_Return'], label='Rule-Based')
        if ml_return is not None:
            ml_cum_return = (ml_df['Close'].pct_change().fillna(0) * ml_df['Predicted'].shift(1).fillna(0) + 1).cumprod()
            plt.plot(ml_cum_return, label='ML Strategy')
        plt.title(f"Strategy Comparison: {stock_name}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f"{stock_name}_comparison.png"))
        plt.close()

# Save summary CSV
summary_df = pd.DataFrame(summary)
summary_df.to_csv(os.path.join(OUTPUT_DIR, "Comparison_Summary.csv"), index=False)
print("Comparison complete. Summary and plots saved to Comparison_Results folder.")
