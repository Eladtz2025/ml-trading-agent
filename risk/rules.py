"""Risk and exposure utility checks for backtests.

These helpers operate on either Pandas ``Series`` objects or ``DataFrame``
containers with the expected columns.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

_TRADING_DAYS_PER_YEAR = 252


def _select_series(
    snap: pd.Series | pd.DataFrame,
    *,
    metric: str,
    candidates: Iterable[str] = (),
) -> pd.Series:
    """Return a numeric series for the requested metric.

    Parameters
    ----------
    snap:
        Either a :class:`pandas.Series` that already contains the desired data or a
        :class:`pandas.DataFrame` with one of the candidate columns.
    metric:
        Human readable metric name used in error messages.
    candidates:
        Ordered collection of column names to search when ``snap`` is a
        :class:`~pandas.DataFrame`.
    """

    if isinstance(snap, pd.Series):
        series = snap
    elif isinstance(snap, pd.DataFrame):
        for name in candidates:
            if name in snap.columns:
                series = snap[name]
                break
        else:
            numeric = snap.select_dtypes(include=[np.number])
            if numeric.empty:
                raise KeyError(
                    f"Unable to locate numeric data for '{metric}'. Provide a Series "
                    "or include one of the expected columns: "
                    + ", ".join(candidates)
                )
            series = numeric.iloc[:, 0]
    else:
        raise TypeError(
            f"Unsupported snapshot type {type(snap)!r} for metric '{metric}'."
        )

    return pd.Series(series, dtype=float)


def max_drawdown(snap: pd.Series | pd.DataFrame) -> float:
    """Compute the maximum drawdown as a negative percentage.

    The function expects cumulative equity values. When supplied with returns it
    will first reconstruct a cumulative equity curve.
    """

    series = _select_series(
        snap,
        metric="max_drawdown",
        candidates=(
            "equity_curve",
            "equity",
            "portfolio_value",
            "nav",
            "close",
        ),
    ).dropna()

    if series.empty:
        return 0.0

    if (series <= 1.0).any() and (series >= -1.0).any():
        # Heuristic: interpret as returns and rebuild cumulative performance.
        series = (1.0 + series).cumprod()

    running_max = series.cummax()
    drawdowns = series / running_max - 1.0
    return float(drawdowns.min())


def volatility(snap: pd.Series | pd.DataFrame) -> float:
    """Annualised volatility of daily returns."""

    returns = _select_series(
        snap,
        metric="volatility",
        candidates=("returns", "return", "pct_change", "log_return"),
    ).dropna()

    if returns.empty and isinstance(snap, pd.Series):
        returns = snap.dropna().pct_change().dropna()
    elif returns.empty:
        returns = _select_series(
            snap,
            metric="volatility",
            candidates=("equity_curve", "equity", "portfolio_value", "nav"),
        ).pct_change().dropna()

    if returns.empty:
        return 0.0

    return float(returns.std(ddof=1) * np.sqrt(_TRADING_DAYS_PER_YEAR))


def exposure(snap: pd.Series | pd.DataFrame) -> float:
    """Proportion of periods with a non-zero position."""

    positions = _select_series(
        snap,
        metric="exposure",
        candidates=("position", "positions", "exposure", "signal"),
    )

    if positions.empty:
        return 0.0

    return float((positions != 0).mean())


def run_checks(snap: pd.Series | pd.DataFrame) -> dict[str, float]:
    """Return the collection of base risk metrics for a snapshot."""

    return {
        "drawdown": max_drawdown(snap),
        "volatility": volatility(snap),
        "exposure": exposure(snap),
    }


if __name__ == "__main__":
    strat_path = "cache/backtest/baseline.parquet"
    try:
        strategy = pd.read_parquet(strat_path)
    except FileNotFoundError:
        raise SystemExit(
            "Baseline backtest not found. Run a backtest first or update the path."
        )

    results = run_checks(strategy)
    print("\n️ MAY RISKS –", results)
