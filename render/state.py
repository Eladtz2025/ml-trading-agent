"""State helpers shared across the Streamlit applications."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import joblib
import pandas as pd

from data.get_data_yahoo import fetch_data
from models.xgb_optuna import train_optuna

MODEL_PATH = Path("models/latest_model.joblib")


def load_data(symbol: str, start: date, end: date) -> pd.DataFrame:
    return fetch_data(symbol, start.isoformat(), end.isoformat())


def load_model() -> object:
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        X = pd.DataFrame([[1, 2, 3, 4, 5]], columns=["O", "H", "L", "C", "V"])
        y = pd.Series([1])
        model = train_optuna(X, y, n_trials=1)
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        return model
