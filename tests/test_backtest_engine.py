"""Tests for the enhanced backtest configuration."""

from __future__ import annotations

import pandas as pd

from backtest.core import BacktestConfig, simple_backtest


def test_simple_backtest_next_open_fill() -> None:
    df = pd.DataFrame(
        {
            "signal": [1, 1, -1, 0],
            "open": [100, 101, 102, 100],
            "close": [101, 102, 101, 99],
        }
    )

    config = BacktestConfig(latency=1, slippage_bps=5, capital=100_000)
    result = simple_backtest(df, config=config)

    assert "execution_price" in result.columns
    assert len(result) == len(df)
    # Ensure latency shift applied
    assert result.loc[0, "position"] == 0
    assert result.loc[1, "position"] == 1
    assert result.loc[1, "execution_price"] == df.loc[1, "open"] * (1 + config.slippage_bps / 10_000)


def test_simple_backtest_close_fill() -> None:
    df = pd.DataFrame(
        {
            "signal": [0, 1, 1],
            "open": [10, 10.5, 11],
            "close": [10.2, 10.7, 11.5],
        }
    )

    config = BacktestConfig(latency=0, fill_logic="close")
    result = simple_backtest(df, config=config)

    assert (result["transaction_costs"] >= 0).all()


def test_backtest_config_roundtrip() -> None:
    payload = {"latency": 2, "slippage_bps": 3.5, "capital": 50_000.0, "fill_logic": "close"}
    cfg = BacktestConfig.from_dict(payload)
    assert cfg.to_dict() == payload
