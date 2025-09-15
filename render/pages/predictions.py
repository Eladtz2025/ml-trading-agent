import streamlit as st
from ...state import load_data, load_model
from ...utils import plot_ohlc, plot_predictions
import pandas as pd

st.title("Predictions Explorer")
symbol = st.text_input("Symbol", value="AAPL")
start = st.date_input("Start", value=pd.to_datetime("2022-01-01"))
end = st.date_input("End", value=pd.to_datetime("2023-01-01"))
if st.button("Run Prediction"):
    df = load_data(symbol, start, end)
    model = load_model()
    preds = model.predict(df[["O", "H", "L", "C", "V"]])
    st.plotly_chart(plot_ohlc(df))
    st.plotly_chart(plot_predictions(df, preds))