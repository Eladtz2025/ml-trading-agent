"""Regression tests for MACD and ATR feature plugins."""

from __future__ import annotations

import pandas as pd
import pytest

from features.atr import atr
from features.macd import macd


def _sample_ohlc() -> pd.DataFrame:
    data = {
        "close": [100, 101, 102, 103, 102, 101, 102, 104, 105, 104],
        "high": [101, 102, 103, 104, 103, 102, 103, 105, 106, 105],
        "low": [99, 100, 101, 102, 101, 100, 101, 103, 104, 103],
    }
    return pd.DataFrame(data)


def test_macd_outputs_expected_columns() -> None:
    df = _sample_ohlc()
    result = macd(df)

    assert list(result.columns) == ["macd", "signal", "hist"]
    # sanity check non-zero values
    assert pytest.approx(result["macd"].iloc[-1], rel=1e-4) != 0


def test_atr_requires_columns() -> None:
    with pytest.raises(KeyError):
        atr(pd.DataFrame({"close": [1, 2, 3]}))


def test_atr_returns_positive_series() -> None:
    df = _sample_ohlc()
    result = atr(df)

    assert "atr" in result.columns
    assert (result["atr"] >= 0).all()
