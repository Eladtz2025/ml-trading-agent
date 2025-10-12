"""A lightweight backtesting simulator used in tests and notebooks."""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate(preds: pd.Series, prices: pd.Series) -> pd.DataFrame:
    """Simulate a simple long/short strategy.

    Parameters
    ----------
    preds:
        Series representing the trading signal. Positive values indicate a
        long position while negative values indicate a short position.
    prices:
        Series of asset prices aligned with ``preds``.

    Returns
    -------
    DataFrame
        DataFrame containing the strategy returns and cumulative equity curve.
    """

    if preds.empty or prices.empty:
        raise ValueError("Predictions and prices must not be empty")

    preds, prices = preds.align(prices, join="inner")
    signal = preds.shift(1).fillna(0)
    price_returns = prices.pct_change().fillna(0)
    strategy_returns = signal * price_returns
    equity_curve = (1 + strategy_returns).cumprod()

    return pd.DataFrame({
        "signal": signal,
        "returns": strategy_returns,
        "equity_curve": equity_curve,
    })


if __name__ == "__main__":
    index = pd.date_range("2023-01-01", periods=5, freq="D")
    demo_prices = pd.Series(np.linspace(100, 110, len(index)), index=index)
    demo_preds = pd.Series([0, 1, -1, 1, 0], index=index)
    result = simulate(demo_preds, demo_prices)
    print(result)
