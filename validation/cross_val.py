"""Time series cross-validation utilities."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import TimeSeriesSplit


def time_series_cv(
    X: pd.DataFrame | np.ndarray,
    y: pd.Series | np.ndarray,
    model_cls,
    *,
    n_splits: int = 5,
) -> float:
    """Perform time-series aware cross validation and return the mean accuracy."""

    X_values = X.to_numpy() if isinstance(X, pd.DataFrame) else np.asarray(X)
    y_values = y.to_numpy() if isinstance(y, pd.Series) else np.asarray(y)

    tscv = TimeSeriesSplit(n_splits=n_splits)
    scores: list[float] = []

    for train_idx, test_idx in tscv.split(X_values):
        X_train, y_train = X_values[train_idx], y_values[train_idx]
        X_test, y_test = X_values[test_idx], y_values[test_idx]

        model = model_cls()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        scores.append(accuracy_score(y_test, preds))

    return float(np.mean(scores))
