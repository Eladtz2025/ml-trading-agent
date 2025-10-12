"""Utilities for computing the Relative Strength Index (RSI)."""

from __future__ import annotations

import pandas as pd


def _validate_window(window: int) -> int:
    """Validate and normalise the RSI lookback window."""

    if not isinstance(window, int):
        raise TypeError("window must be an integer")
    if window <= 0:
        raise ValueError("window must be greater than zero")
    return window


def compute_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """Compute the Relative Strength Index for a price series.

    Parameters
    ----------
    prices:
        Series of prices ordered by time.
    window:
        Lookback window used to calculate the rolling averages.

    Returns
    -------
    pandas.Series
        RSI values in the range ``[0, 100]``.  The first ``window`` values
        default to ``50`` which represents a neutral state.
    """

    window = _validate_window(window)
    prices = prices.astype(float)

    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    rsi = rsi.fillna(50.0)
    rsi = rsi.clip(lower=0, upper=100)

    # When the average loss is zero we are in a persistent up-trend and the
    # RSI should read 100.  Similarly, when both average gain and loss are
    # zero the price is flat and we report a neutral value of 50.
    rsi = rsi.where(avg_loss != 0, 100.0)
    neutral_mask = (avg_gain == 0) & (avg_loss == 0)
    rsi = rsi.where(~neutral_mask, 50.0)

    rsi.name = "rsi"
    return rsi


__all__ = ["compute_rsi"]
