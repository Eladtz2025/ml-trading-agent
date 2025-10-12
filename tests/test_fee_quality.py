"""Tests for fee quality validation utilities."""

from __future__ import annotations

import pandas as pd

from data.fees_quality import detect_fee_anomalies, evaluate_fee_quality


def test_fee_quality_identifies_negative_and_missing() -> None:
    df = pd.DataFrame({
        "fees": [0.1, 0.1, -0.2, None, 0.15],
    })

    report = evaluate_fee_quality(df)

    assert report.total_records == 5
    assert report.negative_fees == 1
    assert report.missing_values == 1


def test_fee_anomalies_flags_large_changes() -> None:
    df = pd.DataFrame({
        "fees": [0.1, 0.11, 0.12, 0.6, 0.61],
    })

    mask = detect_fee_anomalies(df, z_threshold=2.0)
    assert mask.iloc[3]
    assert not mask.iloc[0]
