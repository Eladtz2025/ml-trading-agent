"""Streamlit dashboard that augments metrics with an agent summary."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

REPORT_PATHS = [
    Path("reports/latest_backtest.csv"),
    Path("reports/latest_backtest.tsv"),
    Path("reports/latest.csv"),
]
SHAP_PATH = Path("reports/shap_importance.csv")
CONFUSION_PATH = Path("reports/confusion_matrix.png")
MONITOR_PATH = Path("cache/monitor/status.json")


def _load_report() -> pd.DataFrame:
    for path in REPORT_PATHS:
        if path.exists():
            if path.suffix == ".tsv":
                return pd.read_csv(path, sep="\t")
            return pd.read_csv(path)
    return pd.DataFrame()


def main() -> None:
    st.set_page_config(page_title="Phoenix Agent Dashboard", layout="wide")
    st.title("System Performance Dashboard")

    report = _load_report()
    if not report.empty and {"timestamp", "equity"}.issubset(report.columns):
        st.subheader("Equity Curve")
        fig = px.line(report, x="timestamp", y="equity", title="Equity Curve")
        st.plotly_chart(fig, use_container_width=True)
    elif not report.empty:
        st.write(report.head())
        st.info("Report file found but missing expected columns.")
    else:
        st.warning("No performance report found.")

    st.subheader("Feature Importance (SHAP)")
    if SHAP_PATH.exists():
        shap_df = pd.read_csv(SHAP_PATH)
        st.dataframe(shap_df)
    else:
        st.info("No SHAP importance file available.")

    st.subheader("Confusion Matrix")
    if CONFUSION_PATH.exists():
        st.image(str(CONFUSION_PATH))
    else:
        st.info("Confusion matrix not generated yet.")

    st.subheader("Drift Status")
    if MONITOR_PATH.exists():
        st.json(pd.read_json(MONITOR_PATH).to_dict())
    else:
        st.info("No monitoring status available.")

    st.subheader("🧠 Phoenix Agent Panel")
    st.markdown("**Market Summary:**")
    st.info("Volatility elevated, macro sentiment neutral. Monitoring risk-on assets.")

    st.markdown("**Today's Plan:**")
    st.success("Scan mid-cap breakout patterns, avoid high-beta tech, monitor liquidity shifts.")

    st.markdown("**Agent Recommendation:**")
    st.code("Long: $XLF (2.1% allocation)\nHedge: Short $QQQ (1.2%)", language="text")


if __name__ == "__main__":
    main()
