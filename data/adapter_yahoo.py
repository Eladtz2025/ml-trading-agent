"""Thin wrapper around the :mod:`yfinance` client with caching."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import yfinance as yf

CACHE_DIR = Path("artifacts/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _hash_params(symbol: str, start: str, end: str, interval: str) -> str:
    key = f"{symbol}_{start}_{end}_{interval}"
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def get(symbol: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    """Download OHLCV data and cache it on disk."""

    cache_file = CACHE_DIR / f"{_hash_params(symbol, start, end, interval)}.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)

    data = yf.download(symbol, start=start, end=end, interval=interval, progress=False)
    if data.empty:
        raise ValueError(f"No data for {symbol} between {start} and {end}.")

    data = data.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        }
    ).reset_index()

    data = data.rename(columns={"Date": "timestamp"})
    data.to_parquet(cache_file, index=False)

    return data
