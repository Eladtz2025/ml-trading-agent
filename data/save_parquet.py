"""Helpers for persisting market data in Parquet format."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_PATH = Path("cache/data")


def save_parquet(ticker: str, df: pd.DataFrame, *, index_column: str = "date") -> Path:
    """Save *df* using the ticker symbol as filename."""

    destination = DEFAULT_PATH / f"{ticker.upper()}.parquet"
    destination.parent.mkdir(parents=True, exist_ok=True)

    data = df.copy()
    if index_column in data.columns:
        data = data.set_index(index_column)

    data.to_parquet(destination)
    return destination


if __name__ == "__main__":  # pragma: no cover - quick manual test
    sample = pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=3, freq="D"),
        "close": [100, 101, 102],
    })
    saved_path = save_parquet("spy", sample)
    print("Data saved to:", saved_path)
