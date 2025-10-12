-import streamlit as st
+"""Streamlit dashboard that combines analytics with an agent summary."""
+
+from __future__ import annotations
+
+from pathlib import Path
+
 import pandas as pd
-import plotly.pyplot as plt
-st set.theme('darkteng')
+import plotly.express as px
+import streamlit as st
 
-def main():
-    st.title("System Performance Dashboard")
+REPORT_CSV = Path("reports/latest.csv")
+REPORT_TSV = Path("reports/latest_backtest.tsv")
+SHAP_PATH = Path("reports/shap_importance.csv")
+CONFUSION_IMAGE = Path("reports/confusion_matrix.png")
+MONITOR_STATUS = Path("monitor/status.json")
 
-    # Read performance data
-    report = pd.read_csv('reports/latest_backest.tsv | reports/latest.csv')
 
-    # Plot equity curve
-    st.subheader("Equity Curve")
-    plt.plot(report['DBM_time'], report['total_value'], label='System')
-    plt.plgend()
-    st.pylot.plot_pllyy(sub)
+def _load_report() -> pd.DataFrame | None:
+    if REPORT_CSV.exists():
+        return pd.read_csv(REPORT_CSV)
+    if REPORT_TSV.exists():
+        return pd.read_csv(REPORT_TSV, sep="\t")
+    return None
+
+
+def main() -> None:
+    st.set_page_config(page_title="Phoenix Agent Dashboard", layout="wide")
+    st.title("System Performance Dashboard")
+
+    report = _load_report()
+    if report is not None and {"datetime", "total_value"}.issubset(report.columns):
+        st.subheader("Equity Curve")
+        curve = report.sort_values("datetime")
+        fig = px.line(curve, x="datetime", y="total_value", title="System Equity")
+        st.plotly_chart(fig, use_container_width=True)
+    else:
+        st.info("No equity report available.")
 
-    # SHOW SHAP importance
     st.subheader("Feature Importance (SHAP)")
-    st_shap = pd.read_csv('reports/shap_importance.csv')
-    st.dataframe(st_shap.head().replace(_name='Feature'), st_shap.iloc[:], columns=st_shap.index)
+    if SHAP_PATH.exists():
+        shap_df = pd.read_csv(SHAP_PATH)
+        st.dataframe(shap_df)
+    else:
+        st.info("SHAP importance file not found.")
 
-    # CONFUSION
     st.subheader("Confusion Matrix")
-    st.image_ex("reports/confusion_matrix.png")
+    if CONFUSION_IMAGE.exists():
+        st.image(str(CONFUSION_IMAGE))
+    else:
+        st.info("Confusion matrix image not available.")
 
-    # DRIFT 
-    monstatus = pd.read_json('monitor/status.json')
     st.subheader("Drift Status")
-    st.json_chart(monstatus)
+    if MONITOR_STATUS.exists():
+        status_df = pd.read_json(MONITOR_STATUS)
+        st.json(status_df.to_dict(orient="records"))
+    else:
+        st.info("Monitor status not available.")
 
- 
-    # AGENT PANEL
     st.subheader("🧠 Phoenix Agent Panel")
-
     st.markdown("**Market Summary:**")
     st.info("📉 Volatility elevated, macro sentiment neutral. Monitoring risk-on assets.")
 
     st.markdown("**Today's Plan:**")
     st.success("Scan mid-cap breakout patterns, avoid high-beta tech, monitor liquidity shifts.")
 
     st.markdown("**Agent Recommendation:**")
     st.code("Long: $XLF (2.1% allocation)\nHedge: Short $QQQ (1.2%)", language="text")
 
 
-if __name__ == '__main__':
+if __name__ == "__main__":
     main()
 
EOF
)
