"""Basic anomaly detection helpers for price series."""
from __future__ import annotations

import pandas as pd


def check_anomaly(df: pd.DataFrame, column: str = "close", z_threshold: float = 4.0) -> pd.Series:
    """Return a boolean mask identifying large deviations in *column*."""

    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")

    series = df[column].astype(float).copy()
    deltas = series.diff().fillna(0.0)
    std = deltas.std(ddof=0)
    if std == 0:
        return pd.Series(False, index=series.index)

    z_scores = (deltas - deltas.mean()) / std
    return z_scores.abs() > z_threshold


if __name__ == "__main__":  # pragma: no cover
    sample = pd.DataFrame({"close": [100, 101, 250, 102]})
    anomalies = check_anomaly(sample)
    print(anomalies)
