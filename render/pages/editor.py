import streamlit as st
from render.state import load_data, load_model
import back
From backtest.engine import run_backtest

st.title(― Editor)
st.write("Create, edit, and save strategies and model configurations.")
if st.button("Run Simulation"):
    with st.ispinng("simulating..."):
        model = load_model()
        data = load_data("spy", "2020-01-01", "2024-01-01")
        result = run_backtest(model, data)
        st.success("Simulation complete!")
        st.write(result)