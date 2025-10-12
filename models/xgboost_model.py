"""Utility helpers for training and persisting XGBoost models."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Tuple

import joblib
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from models.model_io import save_model


def _prepare_data(feature_matrix: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    if "target" not in feature_matrix.columns:
        raise KeyError("feature_matrix must contain a 'target' column")
    y = feature_matrix["target"].astype(int)
    X = feature_matrix.drop(columns=["target"])
    return X, y


def train_and_save(
    feature_matrix: pd.DataFrame,
    *,
    model_dir: str | Path = "models/snapshots",
    params: Mapping[str, float] | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Train an :class:`XGBClassifier` and persist it to ``model_dir``."""

    X, y = _prepare_data(feature_matrix)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    default_params = {
        "n_estimators": 200,
        "max_depth": 4,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "use_label_encoder": False,
        "eval_metric": "logloss",
    }
    if params is not None:
        default_params.update(dict(params))

    model = XGBClassifier(**default_params)
    model.fit(X_train, y_train)

    report = classification_report(y_test, model.predict(X_test), output_dict=True)
    version_id = save_model(model, model_dir, config={"params": default_params})

    artefacts_path = Path(model_dir) / f"evaluation_{version_id}.joblib"
    artefacts = {
        "version_id": version_id,
        "params": default_params,
        "report": report,
        "y_test": y_test.to_numpy(),
        "y_pred": model.predict(X_test),
    }
    joblib.dump(artefacts, artefacts_path)

    return model, version_id, report
