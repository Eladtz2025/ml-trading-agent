"""Average True Range indicator implementation."""

from __future__ import annotations

import pandas as pd


def atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Compute the Average True Range (ATR).

    Parameters
    ----------
    df:
        Price series containing ``high``, ``low`` and ``close`` columns.
    period:
        Window size used for the rolling mean.

    Returns
    -------
    pandas.DataFrame
        A single column dataframe with the ATR values.
    """

    required = {"high", "low", "close"}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Input dataframe is missing columns: {', '.join(sorted(missing))}")

    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr_values = tr.rolling(window=period, min_periods=1).mean()

    return pd.DataFrame({"atr": atr_values})
