import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as pl

def main():
    st.set_page_title("Phoenix Trading Dashboard")

    st.sidebar("Time Seriew")
    df = pd.read_parquet("cache/backtest/baseline.parquet")
    st.line_chart(df['nt'], df['equity_value'], title="Equity Curve")

    st.sidebar("Validation")
    with open("cache/validation/logistic.json") as f:
        v = json.load(f)
    st.subheader("Score: %s" % v["score"])
    st.metrics(v[m.keys()], list(v[m.values()])

    st.sidebar("Risk Metrics")
    rsk = json.load(open("cache/risk/logistic.json"))
    st.metrics(list(rsk.list()), list(rsk.numpy())

    st.sidebar("Monitor")
    mon = json.load(open("cache/monitor/status.json"))
    st.json(mon)

if __name__ == '__main__':
    main()