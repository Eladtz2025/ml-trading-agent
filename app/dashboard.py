"""Streamlit dashboard for monitoring Phoenix trading models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import streamlit as st

BACKTEST_PATH = Path("cache/backtest/baseline.parquet")
VALIDATION_PATH = Path("cache/validation/logistic.json")
RISK_PATH = Path("cache/risk/logistic.json")
MONITOR_PATH = Path("cache/monitor/status.json")


def _load_json(path: Path) -> Dict[str, Any]:
    """Load JSON content from ``path`` if it exists."""
    if not path.exists():
        return {}
    with path.open() as file:
        return json.load(file)


def _load_backtest(path: Path) -> pd.DataFrame | None:
    """Load a backtest parquet file if available."""
    if not path.exists():
        return None
    try:
        return pd.read_parquet(path)
    except Exception as exc:  # pragma: no cover - defensive
        st.warning(f"Unable to load backtest results: {exc}")
        return None


def main() -> None:
    """Render the Streamlit dashboard."""

    st.set_page_config(page_title="Phoenix Trading Dashboard", layout="wide")
    st.title("Phoenix Trading Dashboard")

    sidebar = st.sidebar
    sidebar.header("Sections")
    sidebar.write("Select the section to explore the latest metrics.")

    backtest_df = _load_backtest(BACKTEST_PATH)
    if backtest_df is not None and {"nt", "equity_value"}.issubset(backtest_df.columns):
        st.subheader("Equity Curve")
        chart_df = backtest_df.set_index("nt")["equity_value"]
        st.line_chart(chart_df, height=320)
    else:
        st.info("Backtest results are not available.")

    validation_data = _load_json(VALIDATION_PATH)
    if validation_data:
        st.subheader("Validation Metrics")
        metrics = {k: v for k, v in validation_data.items() if isinstance(v, (int, float))}
        cols = st.columns(max(len(metrics), 1))
        for col, (label, value) in zip(cols, metrics.items()):
            col.metric(label, value)
        if len(validation_data) != len(metrics):
            st.json(validation_data)
    else:
        st.info("Validation metrics are not available.")

    risk_data = _load_json(RISK_PATH)
    if risk_data:
        st.subheader("Risk Metrics")
        cols = st.columns(max(len(risk_data), 1))
        for col, (label, value) in zip(cols, risk_data.items()):
            if isinstance(value, (int, float)):
                col.metric(label, value)
            else:
                col.write({label: value})
    else:
        st.info("Risk metrics are not available.")

    monitor_data = _load_json(MONITOR_PATH)
    st.subheader("Monitor")
    if monitor_data:
        st.json(monitor_data)
    else:
        st.info("Monitoring data is not available.")


if __name__ == "__main__":
    main()
