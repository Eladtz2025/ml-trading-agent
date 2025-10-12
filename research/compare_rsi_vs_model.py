"""Quick comparison of a simple RSI strategy versus an XGBoost model."""

from __future__ import annotations

import pandas as pd

from backtest.run import run_backtest
from data.get_data_yahoo import fetch_data
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.xgb import XGBModel


def build_dataset(ticker: str, start: str = "2020-01-01", end: str = "2024-01-01") -> pd.DataFrame:
    data = fetch_data(ticker, start, end)
    frame = pd.DataFrame(index=data.index)
    frame["close"] = data["Close"] if "Close" in data.columns else data["close"]
    frame["rsi"] = compute_rsi(frame["close"])
    frame["returns"] = frame["close"].pct_change().fillna(0)
    frame["label"] = (label_next_bar(frame["close"]).reindex(frame.index).fillna(0) > 0).astype(int)
    return frame.dropna()


def compare(ticker: str = "SPY") -> None:
    dataset = build_dataset(ticker)
    features = dataset[["rsi", "returns"]]
    labels = dataset["label"].astype(int)

    rsi_signal = (features["rsi"] < 30).astype(int)
    rsi_accuracy = float((rsi_signal == labels).mean())

    model = XGBModel()
    model_summary, _ = run_backtest(features, labels, model)

    print(f"RSI accuracy: {rsi_accuracy:.3f}")
    print("Model summary:", model_summary)


if __name__ == "__main__":  # pragma: no cover
    compare()
