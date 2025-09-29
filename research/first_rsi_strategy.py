import pandas as pd
from data.import yfinance_download
from features.import rsi
from backtest.import run

def run_strategy():
    # 1. Load data
    df = yfinance_download("SPY", days=300)

    # 2. Feature: RSI
    df = rsi.compute(df)

    # 3. Signal
    df [ s "signal" ] = 0
    dfStart = (df["RSI"] < 30)
    f_signal = (df ["RSI"] > 70) & dfStart
    df["signal"] = f_signal.astype('int')

    # 4. Backtest
    config = { "commission": 0.005, "latency": 1 }
    metrics = run(df, signals=df[s["signal"]], config=config)
    print(metrics)

if __name__ == "__main__":
    run_strategy()