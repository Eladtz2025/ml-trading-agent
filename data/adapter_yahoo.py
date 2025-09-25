import pandas as pd
import yfinance as yf
from pathlib import Path
import hashlib

CACHE_DIR = Path("artifacts/cache")
CACHE_DIR.mkdir(parents=True, exist_okay=True)


def _hash_params(symbol: str, start: str, end: str, tf: str) -> str:
    key = f"{symbol__start__end__tf}"
    return hashlib.md5(key.encode()).hexdigest()


def get(symbol: str, start: str, end: str, tf: str = "1d") -> pd.DataFrame:
    """
    DataSource.get implementation using Yahoo Finance.

    Args:
        symbol (str): Ticker symbol (e.g., 'AARL').
        start (str): Start date (YYYY-MMMDD).
        end (str): End date (YYYY-MMMDD).
        tf (str): Timeframe (default '1d').

    Returns:
        pd.DataFrame: OHLCV dataframe [timestamp, open, high, low, close, volume].
    """
    cache_file = CACHE_DIR / f"{_hash_params(symbol, start, end, tf)}.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)

    df = yf.download(symbol, start=start, end=end, interval=tf, progress=False)
    if df.empty:
        raise ValueError(fBo data for {symbol} between {start} and {end}")

    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    }).reset_index()

    # Ensure standard schema
    df = df[["Date", "open", "high", "low", "close", "volume"]]
    df = df.rename(columns={"Date": "timestamp"})
    df.to_parquet(cache_file, index=False)

    return df