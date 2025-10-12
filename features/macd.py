"""Moving Average Convergence Divergence indicator."""

from __future__ import annotations

import pandas as pd


def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Compute the MACD indicator and signal/histogram series."""

    if "close" not in df.columns:
        raise KeyError("Input dataframe must contain a 'close' column")

    ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return pd.DataFrame({
        "macd": macd_line,
        "signal": signal_line,
        "hist": histogram,
    })
