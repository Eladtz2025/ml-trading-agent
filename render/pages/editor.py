import streamlit as st
st.title("🔏 Strategy Editor")
st.text_area("YAML
Configuration:
  strategy: mean_reversion
  window: 14", height=300)
st.button("Run Backtest")