"""Helpers for constructing performance metric tables."""

from __future__ import annotations

import math

import pandas as pd


def _max_drawdown(equity: pd.Series) -> float:
    running_max = equity.cummax()
    drawdowns = equity / running_max - 1.0
    return float(abs(drawdowns.min()))


def build_metrics_table(
    backtest_frame: pd.DataFrame,
    *,
    periods_per_year: int = 252,
) -> pd.DataFrame:
    """Construct a summary statistics table from the backtest frame."""

    if backtest_frame.empty:
        raise ValueError("Backtest frame is empty")

    strategy_returns = backtest_frame["strategy_return"].astype(float)
    equity_curve = (1 + strategy_returns).cumprod()
    pnl = backtest_frame["pnl"].astype(float)

    annualised_return = (equity_curve.iloc[-1] ** (periods_per_year / len(strategy_returns))) - 1
    volatility = strategy_returns.std(ddof=0) * math.sqrt(periods_per_year)
    sharpe = annualised_return / volatility if volatility else 0.0
    max_drawdown = _max_drawdown(equity_curve)
    calmar = annualised_return / max_drawdown if max_drawdown else 0.0

    turnover = backtest_frame["position"].diff().abs().sum() / (2 * len(backtest_frame))
    avg_daily_pnl = pnl.mean()

    table = pd.DataFrame(
        {
            "sharpe": [sharpe],
            "calmar": [calmar],
            "max_drawdown": [max_drawdown],
            "turnover": [turnover],
            "avg_daily_pnl": [avg_daily_pnl],
            "annual_return": [annualised_return],
        }
    )

    return table
