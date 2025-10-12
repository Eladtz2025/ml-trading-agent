"""Feature pipeline orchestration helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from infra import utils


def _load_raw_data(data_path: str | Path) -> pd.DataFrame:
    """Load raw data from a CSV or parquet file."""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def run_features(feature_pack: str | Path, data_path: str | Path) -> pd.DataFrame:
    """Load data, apply the configured feature functions and return the dataframe."""
    df = _load_raw_data(data_path)
    feature_functions = utils.load_feature_functions(feature_pack)

    utils.apply_features(df, feature_functions)
    return df
