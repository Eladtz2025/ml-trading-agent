"""Initial training script used during exploratory analysis."""

from __future__ import annotations

import pandas as pd

from data.get_data_yahoo import fetch_data
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.xgboost_model import train_and_save


def build_feature_matrix(ticker: str = "SPY") -> pd.DataFrame:
    data = fetch_data(ticker, "2020-01-01", "2024-01-01")
    frame = pd.DataFrame(index=data.index)
    frame["close"] = data["Close"] if "Close" in data.columns else data["close"]
    frame["rsi"] = compute_rsi(frame["close"])
    frame["returns"] = frame["close"].pct_change().fillna(0)
    frame["target"] = (label_next_bar(frame["close"]).reindex(frame.index).fillna(0) == 1).astype(int)
    return frame.dropna()


def main() -> None:
    features = build_feature_matrix()
    train_and_save(features)


if __name__ == "__main__":  # pragma: no cover
    main()
