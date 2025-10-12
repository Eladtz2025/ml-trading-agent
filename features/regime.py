"""Utilities for computing simple market regimes."""

from __future__ import annotations

import warnings

import pandas as pd
from sklearn.cluster import KMeans

DEFAULT_N_REGIMES = 3


def compute_regime(df: pd.DataFrame, n_regimes: int = DEFAULT_N_REGIMES) -> pd.Series:
    """Cluster log returns into discrete regimes."""

    if n_regimes <= 0:
        raise ValueError("n_regimes must be positive")

    if "close" in df.columns:
        close = df["close"]
    elif "Close" in df.columns:
        close = df["Close"]
    else:
        raise KeyError("DataFrame must contain a 'close' column")

    returns = close.pct_change().fillna(0).to_frame("returns")

    if len(returns) < n_regimes:
        warnings.warn(
            "Not enough samples to compute regimes; returning zeros.",
            RuntimeWarning,
            stacklevel=2,
        )
        return pd.Series(0, index=returns.index, name="regime")

    model = KMeans(n_clusters=n_regimes, random_state=42, n_init=10)
    labels = model.fit_predict(returns)
    return pd.Series(labels, index=returns.index, name="regime")


if __name__ == "__main__":
    data = pd.DataFrame({"close": [100, 101, 102, 101, 99, 100]})
    print(compute_regime(data).value_counts())
