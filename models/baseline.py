"""Baseline experiments for quick model comparisons."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import TimeSeriesSplit

DEFAULT_WALK_SPLITS = 4


@dataclass
class BaselineResult:
    """Container storing the per-fold ROC-AUC scores."""

    scores: List[float]

    @property
    def mean(self) -> float:
        return float(np.mean(self.scores)) if self.scores else float("nan")

    @property
    def std(self) -> float:
        return float(np.std(self.scores)) if self.scores else float("nan")


def _to_frame(data: Iterable) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data
    return pd.DataFrame(data)


def _to_series(data: Iterable) -> pd.Series:
    if isinstance(data, pd.Series):
        return data
    return pd.Series(data)


def _run_cv(
    model,
    X: pd.DataFrame,
    y: pd.Series,
    *,
    n_splits: int,
) -> BaselineResult:
    splitter = TimeSeriesSplit(n_splits=n_splits)
    scores: List[float] = []
    for train_idx, test_idx in splitter.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model.fit(X_train, y_train)
        if hasattr(model, "predict_proba"):
            preds = model.predict_proba(X_test)[:, 1]
        else:
            preds = model.predict(X_test)
        score = roc_auc_score(y_test, preds)
        scores.append(float(score))
    return BaselineResult(scores)


def run_baseline(
    X: Iterable,
    y: Sequence,
    *,
    n_splits: int = DEFAULT_WALK_SPLITS,
    model_kwargs: dict | None = None,
) -> BaselineResult:
    """Evaluate a logistic regression model using walk-forward splits."""

    frame = _to_frame(X)
    target = _to_series(y)
    model = LogisticRegression(max_iter=1000, **(model_kwargs or {}))
    return _run_cv(model, frame, target, n_splits=n_splits)


def run_lgbm(
    X: Iterable,
    y: Sequence,
    *,
    n_splits: int = DEFAULT_WALK_SPLITS,
    model_kwargs: dict | None = None,
) -> BaselineResult:
    """Evaluate a LightGBM model using walk-forward splits."""

    frame = _to_frame(X)
    target = _to_series(y)
    default_params = {
        "n_estimators": 200,
        "learning_rate": 0.05,
        "objective": "binary",
    }
    params = {**default_params, **(model_kwargs or {})}
    model = LGBMClassifier(**params)
    return _run_cv(model, frame, target, n_splits=n_splits)


def _load_data(features_path: Path, labels_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    features = pd.read_parquet(features_path)
    labels = pd.read_parquet(labels_path).iloc[:, 0]
    labels.name = "label"
    return features, labels


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Run baseline model experiments")
    parser.add_argument("features", type=Path, help="Path to the feature matrix parquet file")
    parser.add_argument("labels", type=Path, help="Path to the labels parquet file")
    parser.add_argument("--splits", type=int, default=DEFAULT_WALK_SPLITS, help="Number of walk-forward splits")
    args = parser.parse_args()

    X, y = _load_data(args.features, args.labels)

    logistic_scores = run_baseline(X, y, n_splits=args.splits)
    print(f"Logistic Regression ROC-AUC: {logistic_scores.mean:.4f} ± {logistic_scores.std:.4f}")

    lgbm_scores = run_lgbm(X, y, n_splits=args.splits)
    print(f"LightGBM ROC-AUC: {lgbm_scores.mean:.4f} ± {lgbm_scores.std:.4f}")
