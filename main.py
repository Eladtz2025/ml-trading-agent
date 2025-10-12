"""Entry point for running a lightweight end-to-end demo pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from backtest.run import run_backtest
from data import get as load_data
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.dummy import DummyModel

_TIMEFRAME_ALIASES: dict[str, str] = {
    "daily": "1d",
    "1d": "1d",
    "1m": "1m",
}


def load_config(filename: str | Path = "config.yaml") -> dict[str, Any]:
    """Load a YAML configuration file and return its contents as a dict."""

    path = Path(filename)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise TypeError("Configuration file must contain a mapping at the top level")
    return data


def main() -> None:
    """Run a minimal pipeline consisting of data, features, labels and a model."""

    cfg = load_config("packs/example_aplz/config.yaml")

    symbol = str(cfg.get("symbol", "SPY"))
    start = str(cfg.get("start", "2022-01-01"))
    end = str(cfg.get("end", "2023-01-01"))
    timeframe = str(cfg.get("tf_mp", "1d"))
    timeframe = _TIMEFRAME_ALIASES.get(timeframe, timeframe)

    try:
        prices = load_data(symbol, start, end, timeframe)
    except Exception as exc:  # pragma: no cover - defensive for CLI use
        raise RuntimeError(f"Failed to load data for {symbol}: {exc}") from exc

    if "C" in prices:
        close = prices["C"].astype(float)
    elif "Close" in prices:
        close = prices["Close"].astype(float)
    else:
        raise KeyError("Price data must include a 'C' or 'Close' column")

    features = pd.DataFrame(
        {
            "close": close,
            "rsi": compute_rsi(close, window=14),
        }
    ).dropna()

    if features.empty:
        raise ValueError("Insufficient data to compute features")

    labels = label_next_bar(features["close"])
    model = DummyModel()
    summary, predictions = run_backtest(features[["rsi"]], labels, model)

    print("Backtest summary:")
    for key, value in summary.items():
        print(f"  {key}: {value:.4f}")

    print("\nPredictions head:\n", predictions.head())


if __name__ == "__main__":
    main()
