"""Core primitives for the backtesting engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd


@dataclass
class BacktestConfig:
    """Configuration for basic execution assumptions."""

    latency: int = 1
    slippage_bps: float = 0.0
    capital: float = 1_000_000.0
    fill_logic: Literal["close", "next_open"] = "next_open"


def _apply_slippage(price: pd.Series, slippage_bps: float) -> pd.Series:
    return price * (1 + slippage_bps / 10_000)


def simple_backtest(
    df: pd.DataFrame,
    *,
    signal_col: str = "signal",
    open_col: str = "open",
    close_col: str = "close",
    config: BacktestConfig | None = None,
) -> pd.DataFrame:
    """Return a PnL dataframe applying latency/slippage assumptions."""

    if config is None:
        config = BacktestConfig()

    data = df.copy()
    if signal_col not in data.columns:
        raise KeyError(f"Missing signal column '{signal_col}'")
    if open_col not in data.columns or close_col not in data.columns:
        raise KeyError("Input data must contain open and close prices")

    shifted_signal = data[signal_col].shift(config.latency).fillna(0.0)
    data["position"] = shifted_signal

    if config.fill_logic == "next_open":
        execution_price = data[open_col]
    else:
        execution_price = data[close_col]

    execution_price = _apply_slippage(execution_price, config.slippage_bps)
    data["execution_price"] = execution_price

    data["returns"] = data[close_col].pct_change().fillna(0.0)
    data["strategy_return"] = data["position"] * data["returns"]
    trade_delta = data["position"].diff().abs().fillna(0.0)
    data["transaction_costs"] = trade_delta * (config.slippage_bps / 10_000)
    data["pnl"] = (data["strategy_return"] - data["transaction_costs"]) * config.capital

    return data[[
        "position",
        "execution_price",
        "returns",
        "strategy_return",
        "transaction_costs",
        "pnl",
    ]]
