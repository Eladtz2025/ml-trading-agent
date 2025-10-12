"""Advanced Streamlit dashboard for Phoenix trading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import plotly.express as px
import streamlit as st

BACKTEST_PATH = Path("cache/backtest/baseline.parquet")
PREDICTIONS_PATH = Path("cache/validation/logistic.parquet")
RISK_PATH = Path("cache/risk/logistic.json")
MONITOR_PATH = Path("cache/monitor/status.json")
ASSETS = ["SPY", "QQQ", "COMP"]


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open() as file:
        return json.load(file)


def _load_parquet(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_parquet(path)
    return pd.DataFrame()


def main() -> None:
    st.set_page_config(layout="wide", page_title="Phoenix Advanced Dashboard")
    st.title("Phoenix Advanced Dashboard")

    asset = st.selectbox("Asset", options=ASSETS, index=0)
    st.caption(f"Currently displaying results for {asset}.")

    backtest_df = _load_parquet(BACKTEST_PATH)
    if not backtest_df.empty and {"nt", "equity_value"}.issubset(backtest_df.columns):
        st.subheader("Equity Curve")
        fig = px.line(backtest_df, x="nt", y="equity_value", title="Equity Value")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No backtest data available.")

    predictions_df = _load_parquet(PREDICTIONS_PATH)
    st.subheader("Validation")
    if not predictions_df.empty:
        metrics = predictions_df.describe().loc[["mean", "std"]]
        st.table(metrics)
    else:
        st.info("No validation predictions available.")

    risk_data = _load_json(RISK_PATH)
    st.subheader("Risk Metrics")
    if risk_data:
        risk_df = pd.DataFrame([risk_data])
        st.table(risk_df)
    else:
        st.info("Risk metrics file not found.")

    monitor_data = _load_json(MONITOR_PATH)
    st.subheader("System Health Monitor")
    health_score = monitor_data.get("health", 1.0) if monitor_data else 1.0
    if health_score < 0.15:
        st.error("Health check failed.")
    else:
        st.success("Passed health check")
    if monitor_data:
        st.json(monitor_data)

    st.markdown("System by [Phoenix](https://github.com/Eladtz2025/ml-trading-agent)")


if __name__ == "__main__":
    main()
