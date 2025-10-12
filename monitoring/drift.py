"""Drift diagnostics utilities (PSI and KS tests)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def population_stability_index(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    """Compute the PSI between two distributions."""

    expected = expected.dropna().astype(float)
    actual = actual.dropna().astype(float)

    quantiles = np.linspace(0, 1, bins + 1)
    cut_points = expected.quantile(quantiles).to_numpy()
    cut_points[0] = -np.inf
    cut_points[-1] = np.inf

    expected_counts, _ = np.histogram(expected, bins=cut_points)
    actual_counts, _ = np.histogram(actual, bins=cut_points)

    expected_perc = expected_counts / expected_counts.sum()
    actual_perc = actual_counts / actual_counts.sum()

    mask = (expected_perc > 0) & (actual_perc > 0)
    psi_values = (actual_perc[mask] - expected_perc[mask]) * np.log(actual_perc[mask] / expected_perc[mask])
    return float(psi_values.sum())


def ks_test(expected: pd.Series, actual: pd.Series) -> float:
    """Return the Kolmogorov-Smirnov statistic between two samples."""

    expected_sorted = np.sort(expected.dropna().to_numpy())
    actual_sorted = np.sort(actual.dropna().to_numpy())

    if expected_sorted.size == 0 or actual_sorted.size == 0:
        return 0.0

    all_values = np.concatenate([expected_sorted, actual_sorted])
    cdf_expected = np.searchsorted(expected_sorted, all_values, side="right") / expected_sorted.size
    cdf_actual = np.searchsorted(actual_sorted, all_values, side="right") / actual_sorted.size
    return float(np.max(np.abs(cdf_expected - cdf_actual)))


def compute_drift_metrics(reference: pd.DataFrame, live: pd.DataFrame) -> pd.DataFrame:
    """Compute PSI and KS metrics for overlapping columns."""

    shared_columns = sorted(set(reference.columns).intersection(live.columns))
    records = []
    for column in shared_columns:
        psi = population_stability_index(reference[column], live[column])
        ks = ks_test(reference[column], live[column])
        records.append({"feature": column, "psi": psi, "ks": ks})

    return pd.DataFrame.from_records(records)
