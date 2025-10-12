"""Model evaluation utilities."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

_METRICS = {
    "accuracy": accuracy_score,
    "precision": precision_score,
    "recall": recall_score,
    "roc_auc": roc_auc_score,
}


def _to_numpy(array_like: Any) -> np.ndarray:
    """Convert an array-like object to a NumPy array."""

    if isinstance(array_like, np.ndarray):
        return array_like
    if isinstance(array_like, pd.Series):
        return array_like.to_numpy()
    if isinstance(array_like, pd.DataFrame):
        if array_like.shape[1] != 1:
            raise TypeError("DataFrame predictions must contain exactly one column")
        return array_like.iloc[:, 0].to_numpy()
    if isinstance(array_like, Mapping):
        if not array_like:
            raise TypeError("Mapping predictions cannot be empty")
        first_value = next(iter(array_like.values()))
        return _to_numpy(first_value)
    if isinstance(array_like, (Sequence, Iterable)) and not isinstance(
        array_like, (str, bytes)
    ):
        return np.asarray(list(array_like))
    raise TypeError("Unsupported type for array conversion")


def _extract_backtest_series(preds: Any) -> pd.Series | None:
    """Return a Series that can be used to compute trading returns."""
    if isinstance(preds, pd.DataFrame):
        if "bt_pnd" in preds.columns:
            return preds["bt_pnd"].astype(float)
        if preds.shape[1] == 1:
            return preds.iloc[:, 0].astype(float)
    if isinstance(preds, pd.Series):
        return preds.astype(float)
    if isinstance(preds, Mapping):
        if "bt_pnd" in preds:
            return pd.Series(preds["bt_pnd"], dtype=float)
    if isinstance(preds, np.ndarray):
        return pd.Series(preds.astype(float))
    if isinstance(preds, (Sequence, Iterable)) and not isinstance(preds, (str, bytes)):
        return pd.Series(list(preds), dtype=float)
    return None


def _compute_returns(series: pd.Series | None) -> pd.Series:
    if series is None or series.empty:
        return pd.Series(dtype=float)

    series = series.astype(float)
    # Try log returns when values are positive, otherwise fall back to simple diff
    positive = (series > 0).all()
    if positive:
        with np.errstate(divide="ignore", invalid="ignore"):
            log_returns = np.log(series).diff()
        if not log_returns.isna().all():
            return log_returns.dropna()
    return series.diff().dropna()


def _sharpe_ratio(returns: pd.Series, periods: int = 252) -> float:
    returns = returns.dropna()
    if returns.empty:
        return 0.0
    std = returns.std()
    if std == 0 or np.isnan(std):
        return 0.0
    mean = returns.mean()
    if np.isnan(mean):
        return 0.0
    return float(np.sqrt(periods) * mean / std)


def evaluate(preds: Any, labels: Any) -> dict[str, float]:
    """Calculate a collection of classification and trading metrics."""

    y_pred = _to_numpy(preds)
    y_true = _to_numpy(labels)

    if y_pred.shape != y_true.shape:
        raise ValueError("preds and labels must have the same length")

    results: dict[str, float] = {}
    for key, func in _METRICS.items():
        try:
            value = func(y_true, y_pred)
        except ValueError:
            value = float("nan")
        results[key.upper()] = float(value)

    returns = _compute_returns(_extract_backtest_series(preds))
    results["SHARPE"] = _sharpe_ratio(returns)

    return results
