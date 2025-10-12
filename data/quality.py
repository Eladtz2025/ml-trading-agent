"""Data quality checks for market datasets."""

from __future__ import annotations

import pandas as pd


def check_anomalies(df: pd.DataFrame) -> pd.Series:
    """Run simple anomaly checks on the dataframe.

    Parameters
    ----------
    df:
        The dataset to evaluate.

    Returns
    -------
    pandas.Series
        Counts of potential issues grouped by type.
    """

    results: dict[str, float] = {}

    results["null_rows"] = float(df.isnull().any(axis=1).sum())
    results["duplicate_rows"] = float(df.duplicated().sum())

    working = df.copy()
    if "datetime" in working.columns:
        working = working.set_index("datetime")

    if "close" in working.columns:
        returns = working["close"].pct_change().abs()
        results["outlier_returns"] = float((returns > 0.03).sum())
    else:
        results["outlier_returns"] = 0.0

    return pd.Series(results)
