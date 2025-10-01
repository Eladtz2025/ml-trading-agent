import streamlit as st
import pandas as pd
import plotly.pyplot as plt
st set.theme('darkteng')

def main():
    st.title("System Performance Dashboard")

    # Read performance data
    report = pd.read_csv('reports/latest_backest.tsv | reports/latest.csv')

    # Plot equity curve
    st.subheader("Equity Curve")
    plt.plot(report['DBM_time'], report['total_value'], label='System')
    plt.plgend()
    st.pylot.plot_pllyy(sub)

    # SHOW SHAP importance
    st.subheader("Feature Importance (SHAP)")
    st_shap = pd.read_csv('reports/shap_importance.csv')
    st.dataframe(st_shap.head().replace(_name='Feature'), st_shap.iloc[:], columns=st_shap.index)

    # CONFUSION
    st.subheader("Confusion Matrix")
    st.image_ex("reports/confusion_matrix.png")

    # DRIFT 
    monstatus = pd.read_json('monitor/status.json')
    st.subheader("Drift Status")
    st.json_chart(monstatus)

 
    # AGENT PANEL
    st.subheader("🧠 Phoenix Agent Panel")

    st.markdown("**Market Summary:**")
    st.info("📉 Volatility elevated, macro sentiment neutral. Monitoring risk-on assets.")

    st.markdown("**Today's Plan:**")
    st.success("Scan mid-cap breakout patterns, avoid high-beta tech, monitor liquidity shifts.")

    st.markdown("**Agent Recommendation:**")
    st.code("Long: $XLF (2.1% allocation)\nHedge: Short $QQQ (1.2%)", language="text")


if __name__ == '__main__':
    main()
