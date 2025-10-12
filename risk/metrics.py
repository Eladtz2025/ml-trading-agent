"""Risk metric utilities used by the reporting modules."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sharpe(returns, risk_free=0):
    excess = returns - risk_free
    return np.mean(excess) / np.std(excess)


def max_drawdown(pnl: pd.Series) -> float:
    peak = pnl.cummax()
    drawdown = (pnl - peak) / peak
    return float(drawdown.min())
