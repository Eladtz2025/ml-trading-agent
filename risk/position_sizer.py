"""Position sizing helpers based on ATR-derived stop distances."""
from __future__ import annotations

import numpy as np
import pandas as pd


def size_position(
    data: pd.DataFrame,
    *,
    account_size: float,
    risk_fraction: float = 0.01,
    atr_window: int = 14,
    stop_multiplier: float = 0.5,
) -> pd.Series:
    """Calculate integer position sizes based on ATR risk budgeting."""

    required = {"high", "low", "close"}
    missing = required - set(data.columns)
    if missing:
        raise KeyError(f"Missing columns for position sizing: {', '.join(sorted(missing))}")

    high = data["high"].astype(float)
    low = data["low"].astype(float)
    close = data["close"].astype(float)

    true_range = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = true_range.rolling(window=atr_window, min_periods=1).mean()
    stop_distance = atr * stop_multiplier

    dollar_risk = account_size * risk_fraction
    with np.errstate(divide="ignore", invalid="ignore"):
        raw_size = dollar_risk / stop_distance

    raw_size = raw_size.replace([np.inf, -np.inf], 0.0).fillna(0.0)
    return raw_size.astype(int)
