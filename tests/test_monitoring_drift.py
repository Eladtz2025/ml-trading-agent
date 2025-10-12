"""Tests for PSI and KS drift diagnostics."""

from __future__ import annotations

import pandas as pd

from monitoring.drift import compute_drift_metrics, ks_test, population_stability_index


def test_population_stability_index_zero_for_identical_series() -> None:
    baseline = pd.Series([1, 2, 3, 4, 5])
    assert population_stability_index(baseline, baseline) == 0.0


def test_ks_test_detects_differences() -> None:
    baseline = pd.Series([0, 0, 0, 0])
    shifted = pd.Series([1, 1, 1, 1])
    assert ks_test(baseline, shifted) == 1.0


def test_compute_drift_metrics_returns_dataframe() -> None:
    reference = pd.DataFrame({"feature": [0, 0, 0, 0], "other": [1, 2, 3, 4]})
    live = pd.DataFrame({"feature": [1, 1, 1, 1], "other": [1, 2, 1, 2]})

    metrics = compute_drift_metrics(reference, live)
    assert set(metrics.columns) == {"feature", "psi", "ks"}
    assert (metrics["feature"] == "feature").any()
