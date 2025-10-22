import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def train_and_predict(df, stock_name):
    df = df.copy()

    required_cols = ['RSI', 'MACD', 'Signal_Line', 'SMA20', 'SMA50', 'Volume', 'Close']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"{stock_name} missing columns: {missing}")
        return df, 0, 0, 0, 0

    # convert numeric
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # feature creation
    df['SMA_Ratio'] = df['SMA20'] / df['SMA50']
    df['Volume_Change'] = df['Volume'].pct_change()

    df = df.dropna(subset=['RSI', 'MACD', 'Signal_Line', 'SMA_Ratio', 'Volume_Change', 'Close'])
    if df.empty:
        print(f"{stock_name} - All rows dropped after dropna() (NaN values too many).")
        return df, 0, 0, 0, 0

    # target creation
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df = df.dropna(subset=['Target'])

    features = ['RSI', 'MACD', 'Signal_Line', 'SMA_Ratio', 'Volume_Change']

    X = df[features]
    y = df['Target']

    if X.empty or y.empty:
        print(f"{stock_name} - X or y empty after processing.")
        return df, 0, 0, 0, 0

    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"\n{stock_name} — Accuracy: {acc:.3f}, Precision: {prec:.3f}, Recall: {rec:.3f}, F1: {f1:.3f}")

    df.loc[X_test.index, 'Predicted'] = y_pred
    return df, acc, prec, rec, f1

def run_logistic_model():
    base_dir = os.path.dirname(__file__)
    input_dir = "C:/Users/archa/Music/AlgoTradingProject/Processed"
    output_dir = "C:/Users/archa/Music/AlgoTradingProject/ML_Results"
    os.makedirs(output_dir, exist_ok=True)

    results = []

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            print(f"\n Processing {file}")
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path)

            df, acc, prec, rec, f1 = train_and_predict(df, file.replace('.csv', ''))
            if df.empty:
                continue

            df.to_csv(os.path.join(output_dir, file), index=False)
            results.append({
                'Stock': file.replace('.csv', ''),
                'Accuracy': acc,
                'Precision': prec,
                'Recall': rec,
                'F1_Score': f1
            })

    if results:
        pd.DataFrame(results).to_csv(os.path.join(output_dir, "ML_Summary.csv"), index=False)
        print("\n All stocks processed. Summary saved to ML_Results/ML_Summary.csv")
    else:
        print("\n No results generated — check your processed data.")

if __name__ == "__main__":
    run_logistic_model()
