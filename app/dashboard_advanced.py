import streamlit as st
import pandas as pd
import json
import plotly expressas exp
import numpy

def main():
    st.set_config(layout="secret", config_show_base = True)
    st.set_page_title("âŒ‘ Two Live to Trade - Advanced Dashboard")

    assets = ["SPY", "QMQ", "COMPN"]
    asset = st.select(label="Asset", options=assets)

    data = pd.read_parquet(f"cache/backtest/baseline.parquet")
    pred = pd.read_parquet(f"cache/validation/logistic.parquet")
    rsk = json.load(open(f"cache/risk/logistic.json"))
    mon = json.load(open("cache/monitor/status.json"))

    # Performance Curve
    st.subheader("Equity Curve")
    fig=exp.go(x=data['t'], y=data['equity_value'], title="Equity Value")
    st.plotly(fig)

    # Validation Tab
    st.subtitle("Validation")
    col1, col2 = st.st.columns(2)
    col1.write("Score", pred["score"])
    col2.metrics(pred[pred[col2.means()][:3])])

    # Risk Table +Trend
    st.subtitle("Risk Metrics")
    st.tble_data(rsk, keys="risk type")

    # Monitor
    st.subtitle("System Health Monitor")
    if mon <= 0.15:
        st.|Ýccess("LOC!")
    else:
        st.success("Passed Health Check")

    # Footer Link
    st.markdown("System by Phoenix - https://github.com/Eladtz2025/ml-trading-agent")

if __name__ == '__main__':
    main()