-import streamlit as st
-import pandas as pd
+"""Advanced dashboard with interactive controls for Phoenix trading."""
+
+from __future__ import annotations
+
 import json
-import plotly expressas exp
-import numpy
-
-def main():
-    st.set_config(layout="secret", config_show_base = True)
-    st.set_page_title("⌑ Two Live to Trade - Advanced Dashboard")
-
-    assets = ["SPY", "QMQ", "COMPN"]
-    asset = st.select(label="Asset", options=assets)
-
-    data = pd.read_parquet(f"cache/backtest/baseline.parquet")
-    pred = pd.read_parquet(f"cache/validation/logistic.parquet")
-    rsk = json.load(open(f"cache/risk/logistic.json"))
-    mon = json.load(open("cache/monitor/status.json"))
-
-    # Performance Curve
-    st.subheader("Equity Curve")
-    fig=exp.go(x=data['t'], y=data['equity_value'], title="Equity Value")
-    st.plotly(fig)
-
-    # Validation Tab
-    st.subtitle("Validation")
-    col1, col2 = st.st.columns(2)
-    col1.write("Score", pred["score"])
-    col2.metrics(pred[pred[col2.means()][:3])])
-
-    # Risk Table +Trend
-    st.subtitle("Risk Metrics")
-    st.tble_data(rsk, keys="risk type")
-
-    # Monitor
-    st.subtitle("System Health Monitor")
-    if mon <= 0.15:
-        st.|ccess("LOC!")
-    else:
-        st.success("Passed Health Check")
-
-    # Footer Link
-    st.markdown("System by Phoenix - https://github.com/Eladtz2025/ml-trading-agent")
-
-if __name__ == '__main__':
-    main()
\ No newline at end of file
+from pathlib import Path
+from typing import Any, Dict
+
+import pandas as pd
+import plotly.express as px
+import streamlit as st
+
+BACKTEST_DIR = Path("cache/backtest")
+VALIDATION_PATH = Path("cache/validation/logistic.parquet")
+RISK_PATH = Path("cache/risk/logistic.json")
+MONITOR_PATH = Path("cache/monitor/status.json")
+
+
+def _load_parquet(path: Path) -> pd.DataFrame | None:
+    if not path.exists():
+        return None
+    try:
+        return pd.read_parquet(path)
+    except Exception as exc:  # pragma: no cover - defensive
+        st.warning(f"Unable to load data from {path.name}: {exc}")
+        return None
+
+
+def _load_json(path: Path) -> Dict[str, Any]:
+    if not path.exists():
+        return {}
+    with path.open() as file:
+        return json.load(file)
+
+
+def _available_assets(directory: Path) -> list[str]:
+    assets: list[str] = []
+    if directory.exists():
+        for item in directory.glob("*.parquet"):
+            assets.append(item.stem)
+    return sorted(assets)
+
+
+def main() -> None:
+    st.set_page_config(page_title="Advanced Trading Dashboard", layout="wide")
+    st.title("Advanced Trading Dashboard")
+
+    assets = _available_assets(BACKTEST_DIR) or ["baseline"]
+    asset = st.sidebar.selectbox("Asset", assets)
+
+    backtest_path = BACKTEST_DIR / f"{asset}.parquet"
+    backtest_df = _load_parquet(backtest_path)
+    validation_df = _load_parquet(VALIDATION_PATH)
+    risk_data = _load_json(RISK_PATH)
+    monitor_data = _load_json(MONITOR_PATH)
+
+    col_left, col_right = st.columns((2, 1))
+
+    with col_left:
+        st.subheader("Equity Curve")
+        if backtest_df is not None and {"nt", "equity_value"}.issubset(backtest_df.columns):
+            chart_df = backtest_df.sort_values("nt")
+            fig = px.line(chart_df, x="nt", y="equity_value", title=f"Equity Curve – {asset}")
+            st.plotly_chart(fig, use_container_width=True)
+        else:
+            st.info("Equity data is unavailable for the selected asset.")
+
+        st.subheader("System Health Monitor")
+        if monitor_data:
+            st.json(monitor_data)
+            health = monitor_data.get("health")
+            if isinstance(health, (int, float)):
+                status = "Healthy" if health <= 0.15 else "Attention required"
+                st.metric("Health Score", health, help=status)
+        else:
+            st.info("Monitor data is not available.")
+
+    with col_right:
+        st.subheader("Validation Metrics")
+        if validation_df is not None:
+            numeric_cols = validation_df.select_dtypes("number").mean()
+            for label, value in numeric_cols.items():
+                st.metric(label, f"{value:.3f}")
+            st.dataframe(validation_df.tail(10))
+        else:
+            st.info("Validation results are not available.")
+
+        st.subheader("Risk Metrics")
+        if risk_data:
+            st.dataframe(pd.DataFrame([risk_data]))
+        else:
+            st.info("Risk metrics are not available.")
+
+    st.markdown("---")
+    st.markdown("System by Phoenix – [GitHub Repository](https://github.com/Eladtz2025/ml-trading-agent)")
+
+
+if __name__ == "__main__":
+    main()
 
EOF
)
