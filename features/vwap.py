"""Volume Weighted Average Price (VWAP) utilities."""

from __future__ import annotations

import pandas as pd


def compute_vwap(df: pd.DataFrame) -> pd.Series:
    """Compute the cumulative VWAP for a price series."""

    if "close" in df.columns:
        close = df["close"]
    elif "Close" in df.columns:
        close = df["Close"]
    else:
        raise KeyError("DataFrame must contain a 'close' column")

    if "volume" in df.columns:
        volume = df["volume"]
    elif "Volume" in df.columns:
        volume = df["Volume"]
    else:
        raise KeyError("DataFrame must contain a 'volume' column")

    volume = volume.fillna(0)
    price_volume = (close.fillna(method="ffill") * volume).cumsum()
    cumulative_volume = volume.cumsum().replace(0, pd.NA)

    vwap = price_volume / cumulative_volume
    return pd.Series(vwap, index=df.index, name="vwap")


if __name__ == "__main__":
    frame = pd.DataFrame(
        {
            "close": [100, 101, 102, 103],
            "volume": [200, 150, 180, 220],
        }
    )
    print(compute_vwap(frame))
