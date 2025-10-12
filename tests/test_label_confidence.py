"""Tests for labeling confidence utilities."""

from __future__ import annotations

import pandas as pd

from labeling.confidence import assign_with_threshold, probability_from_returns


def test_probability_scaled_between_zero_and_one() -> None:
    returns = pd.Series([-0.2, 0.0, 0.2])
    scores = probability_from_returns(returns, threshold=0.2)
    assert scores.min() == 0.0
    assert scores.max() == 1.0


def test_assign_with_threshold_creates_labels_and_confidence() -> None:
    returns = pd.Series([0.05, -0.08, 0.0])
    df = assign_with_threshold(returns, threshold=0.05)

    assert set(df.columns) == {"label", "confidence"}
    assert df.loc[0, "label"] == 1
    assert df.loc[1, "label"] == -1
