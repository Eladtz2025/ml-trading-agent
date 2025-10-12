"""Utilities for simple next bar price movement labelling."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def _as_series(prices: Iterable[float]) -> pd.Series:
    """Convert ``prices`` to a :class:`pandas.Series` if necessary."""

    if isinstance(prices, pd.Series):
        return prices
    return pd.Series(prices)


def label_next_bar(prices: Iterable[float]) -> pd.Series:
    """Return labels describing the next bar move for a price series.

    A value of ``1`` indicates that the next close is higher, ``-1`` signals
    that it is lower, while ``0`` represents no change or missing data.  The
    final observation is labelled ``0`` because there is no forward bar to
    compare against.
    """

    series = _as_series(prices).astype(float)
    if series.empty:
        return pd.Series(dtype="int8")

    next_close = series.shift(-1)
    delta = next_close - series

    labels = delta.apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    labels = labels.fillna(0).astype("int8")
    labels.name = "label_next_bar"
    return labels


__all__ = ["label_next_bar"]