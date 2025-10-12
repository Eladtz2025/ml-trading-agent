"""Utilities for computing On-Balance Volume (OBV)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_obv(df: pd.DataFrame) -> pd.Series:
    """Compute the On-Balance Volume indicator."""

    if "close" in df.columns:
        close = df["close"]
    elif "Close" in df.columns:
        close = df["Close"]
    else:
        raise KeyError("DataFrame must contain a 'close' column")

    if "volume" in df.columns:
        volume = df["volume"].fillna(0)
    elif "Volume" in df.columns:
        volume = df["Volume"].fillna(0)
    else:
        raise KeyError("DataFrame must contain a 'volume' column")

    direction = np.sign(close.diff().fillna(0))
    obv = (direction * volume).cumsum()
    return pd.Series(obv, index=df.index, name="obv")


if __name__ == "__main__":
    data = pd.DataFrame(
        {
            "close": [100, 101, 102, 101],
            "volume": [1500, 1200, 1800, 1600],
        }
    )
    print(compute_obv(data))
