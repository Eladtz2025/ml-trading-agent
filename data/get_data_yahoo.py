"""Convenience wrappers for downloading market data."""
from __future__ import annotations

from .adapter_yahoo import get as get_from_yahoo
from .save_parquet import save_parquet


def fetch_data(
    ticker: str,
    start: str,
    end: str,
    *,
    source: str = "yahoo",
    cache: bool = True,
):
    """Fetch OHLCV data from the configured source and optionally cache it."""

    if source != "yahoo":
        raise ValueError(f"Unsupported data source: {source}")

    data = get_from_yahoo(ticker, start, end)

    if cache:
        save_parquet(ticker, data, index_column="timestamp")

    return data


if __name__ == "__main__":  # pragma: no cover
    frame = fetch_data("SPY", "2018-01-01", "2023-12-31")
    print(frame.head())
    print(frame.tail())
