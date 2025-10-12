"""Thin wrapper around :class:`xgboost.XGBClassifier`."""

from __future__ import annotations

from typing import Any, Mapping

from xgboost import XGBClassifier


class XGBModel:
    """Provide a convenient interface compatible with the project pipeline."""

    def __init__(self, params: Mapping[str, Any] | None = None) -> None:
        default_params: dict[str, Any] = {
            "n_estimators": 200,
            "max_depth": 4,
            "learning_rate": 0.1,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "use_label_encoder": False,
            "eval_metric": "logloss",
        }
        if params:
            default_params.update(dict(params))
        self.model = XGBClassifier(**default_params)

    def fit(self, X, y) -> "XGBModel":
        self.model.fit(X, y)
        return self

    def predict(self, X):
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X)
            return (proba[:, 1] > 0.5).astype(int)
        return self.model.predict(X)

    def predict_proba(self, X):
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        raise AttributeError("Underlying model does not support probability estimates")
