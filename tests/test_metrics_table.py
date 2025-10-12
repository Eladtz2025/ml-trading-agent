"""Tests for the performance metrics table builder."""

from __future__ import annotations

import pandas as pd
import pytest

from reports.metrics_table import build_metrics_table


def test_build_metrics_table_outputs_expected_columns() -> None:
    frame = pd.DataFrame(
        {
            "position": [0, 1, 1, 0],
            "execution_price": [100, 101, 102, 103],
            "returns": [0.0, 0.01, -0.005, 0.002],
            "strategy_return": [0.0, 0.01, -0.005, 0.0],
            "transaction_costs": [0.0, 0.0001, 0.0001, 0.0],
            "pnl": [0.0, 100.0, -50.0, 0.0],
        }
    )

    table = build_metrics_table(frame, periods_per_year=252)

    assert list(table.columns) == [
        "sharpe",
        "calmar",
        "max_drawdown",
        "turnover",
        "avg_daily_pnl",
        "annual_return",
    ]
    assert table.iloc[0]["turnover"] >= 0


def test_build_metrics_table_raises_for_empty_frame() -> None:
    frame = pd.DataFrame(columns=["position", "execution_price", "returns", "strategy_return", "transaction_costs", "pnl"])
    with pytest.raises(ValueError):
        build_metrics_table(frame)
