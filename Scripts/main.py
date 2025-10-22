# main.py
import os
import subprocess

def run_script(script_name):
    """Utility to run a Python script from Scripts folder"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if os.path.exists(script_path):
        print(f"\nRunning {script_name} ...")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"{script_name} not found!")

if __name__ == "__main__":
    # 1️⃣ Data Ingestion
    run_script("data_ingestion.py")

    # 2️⃣ Technical Indicators Calculation
    run_script("technical_indicators.py")

    # 3️⃣ Rule-based Strategy Backtest
    run_script("rule_based_strategy.py")

    # 4️⃣ Logistic Regression ML Strategy
    run_script("logistic_model.py")

    # 5️⃣ Comparison of Rule-based vs ML Strategy
    run_script("compare_strategies.py")

    print("\nAll steps completed successfully! Check output folders for results.")
