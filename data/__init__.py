"""Utilities for downloading and caching market data."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import pandas as pd
import yfinance as yf

__all__ = ["get"]

_CACHE_DIR: Final[Path] = Path("artifacts")
_COLUMNS: Final[list[str]] = ["Open", "High", "Low", "Close", "Volume"]


class DataSource:
    """Simple wrapper around :mod:`yfinance` with local caching."""

    @staticmethod
    def get(symbol: str, start: str, end: str, tf: str = "1d") -> pd.DataFrame:
        """Retrieve OHLCV data for ``symbol`` and cache it locally."""

        cache_file = _CACHE_DIR / f"raw_{symbol}_{tf}.parquet"
        if cache_file.exists():
            return pd.read_parquet(cache_file)

        raw = yf.Ticker(symbol).history(start=start, end=end, interval=tf)
        if raw.empty:
            raise ValueError("Invalid data fetched from yfinance")

        df = raw[_COLUMNS].copy()
        df.index = pd.to_datetime(df.index)
        df = df.rename(
            columns={
                "Open": "O",
                "High": "H",
                "Low": "L",
                "Close": "C",
                "Volume": "V",
            }
        )

        cache_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file)
        return df


def get(symbol: str, start: str, end: str, tf: str = "1d") -> pd.DataFrame:
    """Public helper for retrieving data via :class:`DataSource`."""

    return DataSource.get(symbol, start, end, tf)
