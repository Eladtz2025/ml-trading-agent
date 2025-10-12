"""Prototype RSI trading strategy used during initial experiments."""

from __future__ import annotations

import pandas as pd

from data.get_data_yahoo import fetch_data
from features.rsi import compute_rsi


def run_strategy(ticker: str = "SPY") -> pd.DataFrame:
    df = fetch_data(ticker, "2020-01-01", "2024-01-01")
    prices = df["Close"] if "Close" in df.columns else df["close"]
    rsi = compute_rsi(prices)

    signals = pd.Series(0, index=rsi.index, name="signal")
    signals[rsi < 30] = 1
    signals[rsi > 70] = -1

    return pd.DataFrame({"price": prices, "rsi": rsi, "signal": signals})


if __name__ == "__main__":  # pragma: no cover
    result = run_strategy()
    print(result.tail())
