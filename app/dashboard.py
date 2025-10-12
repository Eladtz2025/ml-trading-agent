-import streamlit as st
-import pandas as pd
+"""Streamlit dashboard for monitoring Phoenix trading models."""
+
+from __future__ import annotations
+
 import json
-import matplotlib.pyplot as pl
+from pathlib import Path
+from typing import Any, Dict
+
+import pandas as pd
+import streamlit as st
+
+BACKTEST_PATH = Path("cache/backtest/baseline.parquet")
+VALIDATION_PATH = Path("cache/validation/logistic.json")
+RISK_PATH = Path("cache/risk/logistic.json")
+MONITOR_PATH = Path("cache/monitor/status.json")
+
+
+def _load_json(path: Path) -> Dict[str, Any]:
+    """Load a JSON file if it exists, otherwise return an empty dict."""
+    if not path.exists():
+        return {}
+    with path.open() as file:
+        return json.load(file)
+
+
+def _load_backtest(path: Path) -> pd.DataFrame | None:
+    """Load the backtest results if the parquet file exists."""
+    if not path.exists():
+        return None
+    try:
+        return pd.read_parquet(path)
+    except Exception as exc:  # pragma: no cover - defensive guard
+        st.warning(f"Unable to load backtest results: {exc}")
+        return None
+
+
+def main() -> None:
+    st.set_page_config(page_title="Phoenix Trading Dashboard", layout="wide")
+    st.title("Phoenix Trading Dashboard")
+
+    sidebar = st.sidebar
+    sidebar.header("Sections")
 
-def main():
-    st.set_page_title("Phoenix Trading Dashboard")
+    backtest_df = _load_backtest(BACKTEST_PATH)
+    if backtest_df is not None and {"nt", "equity_value"}.issubset(backtest_df.columns):
+        st.subheader("Equity Curve")
+        chart_df = backtest_df.set_index("nt")["equity_value"]
+        st.line_chart(chart_df, height=320)
+    else:
+        st.info("Backtest results are not available.")
 
-    st.sidebar("Time Seriew")
-    df = pd.read_parquet("cache/backtest/baseline.parquet")
-    st.line_chart(df['nt'], df['equity_value'], title="Equity Curve")
+    validation_data = _load_json(VALIDATION_PATH)
+    if validation_data:
+        st.subheader("Validation Metrics")
+        metrics = {k: v for k, v in validation_data.items() if isinstance(v, (int, float))}
+        cols = st.columns(max(len(metrics), 1))
+        for col, (label, value) in zip(cols, metrics.items()):
+            col.metric(label, value)
+        if len(validation_data) != len(metrics):
+            st.json(validation_data)
+    else:
+        st.info("Validation metrics are not available.")
 
-    st.sidebar("Validation")
-    with open("cache/validation/logistic.json") as f:
-        v = json.load(f)
-    st.subheader("Score: %s" % v["score"])
-    st.metrics(v[m.keys()], list(v[m.values()])
+    risk_data = _load_json(RISK_PATH)
+    if risk_data:
+        st.subheader("Risk Metrics")
+        cols = st.columns(max(len(risk_data), 1))
+        for col, (label, value) in zip(cols, risk_data.items()):
+            if isinstance(value, (int, float)):
+                col.metric(label, value)
+            else:
+                col.write({label: value})
+    else:
+        st.info("Risk metrics are not available.")
 
-    st.sidebar("Risk Metrics")
-    rsk = json.load(open("cache/risk/logistic.json"))
-    st.metrics(list(rsk.list()), list(rsk.numpy())
+    monitor_data = _load_json(MONITOR_PATH)
+    st.subheader("Monitor")
+    if monitor_data:
+        st.json(monitor_data)
+    else:
+        st.info("Monitoring data is not available.")
 
-    st.sidebar("Monitor")
-    mon = json.load(open("cache/monitor/status.json"))
-    st.json(mon)
 
-if __name__ == '__main__':
-    main()
\ No newline at end of file
+if __name__ == "__main__":
+    main()
 
EOF
)
