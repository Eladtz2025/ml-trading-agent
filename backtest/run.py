"""Utility helpers for running lightweight backtests in tests."""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np
import pandas as pd


def run_backtest(
    features: pd.DataFrame,
    labels: pd.Series,
    model,
) -> Tuple[dict, pd.Series]:
    """Run a simple backtest using ``model`` and return summary metrics.

    The function is intentionally small in scope – it is aimed at exercising
    the pipeline in tests rather than providing a production-grade simulator.
    The supplied ``model`` must implement a ``fit`` and ``predict`` method
    following the scikit-learn API.
    """

    if not isinstance(features, pd.DataFrame):
        raise TypeError("features must be provided as a pandas.DataFrame")
    if not isinstance(labels, pd.Series):
        raise TypeError("labels must be provided as a pandas.Series")

    if len(features) != len(labels):
        raise ValueError("features and labels must have the same number of rows")

    X = features.to_numpy()
    y = labels.to_numpy()

    if hasattr(model, "fit"):
        model.fit(X, y)

    predictions = np.asarray(model.predict(X), dtype=int)
    preds_series = pd.Series(predictions, index=features.index, name="prediction")

    summary = summarize(labels, preds_series)
    return summary, preds_series


def summarize(y_true: Iterable[int], y_pred: Iterable[int]) -> dict:
    """Return accuracy and hit-rate metrics for the provided predictions."""

    truth = pd.Series(y_true, dtype="int8", name="truth")
    preds = pd.Series(y_pred, dtype="int8", name="prediction")

    if len(truth) == 0:
        raise ValueError("Cannot summarise empty predictions")

    accuracy = float((truth == preds).mean())
    positives = truth == 1
    if positives.any():
        hit_rate = float((preds[positives] == 1).mean())
    else:
        hit_rate = 0.0

    return {"accuracy": accuracy, "hit_rate": hit_rate}


__all__ = ["run_backtest", "summarize"]