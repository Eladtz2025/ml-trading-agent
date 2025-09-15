
import streamlit as st
import pandas as pd
from render.utils import plot_ohlc, plot_predictions
from render.state import load_data, load_model

st.set_page_config(layout="wide", page_title="Phoenix Trading Agent")

st.title("Phoenix Trading Agent - UI")
symbol = st.text_input("Symbol", value="AASC")
start = st.date_input("Start", value=pd.to_datetime("2022-01-01"))
end = st.date_input("End", value=pd.to_datetime("2023-01-01"))
if st.button("Load & Predict"):
    df = load_data(symbol, start, end)
    model = load_model()
    preds = model.predict(df[["O", "H", "L", "C", "V"]])
    st.plotly_chart(plot_ohlc(df))
    st.plotly_chart(plot_predictions(df, preds))