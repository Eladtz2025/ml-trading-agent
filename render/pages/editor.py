import streamlit as st
import pandas as pd
from render.state import load_data, load_model
from backtest.engine import run_backtest

st.title("Pá Editor")
st.write("Create, edit, and save strategies and model configurations.")

symbol = st.text_input("Symbol", value="SPY")
start = st.date_input("Start", value=pd.to_datetime("2020-01-01"))
end = st.date_input("End", value=pd.to_datetime("2024-01-01"))

if st.button("Run Simulation"):

    with st.spinner("Simulating..."):
        model = load_model()
        data = load_data(symbol, start, end)
        result = run_backtest(model, data)
        st.success("Simulation complete!")
        st.write(result)