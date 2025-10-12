"""Streamlit dashboard that surfaces monitoring artefacts."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ARTIFACT_DIR = Path("reports")
MONITOR_DIR = Path("monitor")

st.set_page_config(page_title="Trading System Dashboard", layout="wide")


def _load_first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def _load_equity_curve() -> pd.DataFrame | None:
    candidate = _load_first_existing(
        ARTIFACT_DIR / "latest_backtest.csv",
        ARTIFACT_DIR / "latest.csv",
    )
    if candidate is None:
        return None
    return pd.read_csv(candidate)


def _load_shap() -> pd.DataFrame | None:
    shap_path = ARTIFACT_DIR / "shap_importance.csv"
    if not shap_path.exists():
        return None
    return pd.read_csv(shap_path)


def _load_monitor_status() -> dict | None:
    status_path = MONITOR_DIR / "status.json"
    if not status_path.exists():
        return None
    return pd.read_json(status_path).to_dict(orient="records")


def main() -> None:
    st.title("System Performance Dashboard")

    report = _load_equity_curve()
    if report is not None and {"timestamp", "total_value"}.issubset(report.columns):
        st.subheader("Equity Curve")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=report["timestamp"], y=report["total_value"], name="System")
        )
        fig.update_layout(xaxis_title="Date", yaxis_title="Total Value")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Equity curve artefact not available.")

    shap_values = _load_shap()
    if shap_values is not None:
        st.subheader("Feature Importance (SHAP)")
        st.dataframe(shap_values)
    else:
        st.info("SHAP importance file not found.")

    confusion_path = ARTIFACT_DIR / "confusion_matrix.png"
    if confusion_path.exists():
        st.subheader("Confusion Matrix")
        st.image(str(confusion_path))
    else:
        st.info("Confusion matrix image not generated yet.")

    monitor_status = _load_monitor_status()
    if monitor_status is not None:
        st.subheader("Drift Status")
        st.json(monitor_status)
    else:
        st.info("Monitoring status not available.")


if __name__ == "__main__":
    main()
