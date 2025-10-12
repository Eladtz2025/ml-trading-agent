import pandas as pd
import pytest

from backtest.run import summarize


def test_summarize_returns_expected_metrics():
    truth = pd.Series([1, -1, 1, 1, -1], dtype="int8")
    predictions = pd.Series([1, -1, -1, 1, -1], dtype="int8")

    summary = summarize(truth, predictions)

    assert summary["accuracy"] == pytest.approx(0.8)
    assert summary["hit_rate"] == pytest.approx(2 / 3)