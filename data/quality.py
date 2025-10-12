+"""Data quality checks for market datasets."""
+
+from __future__ import annotations
+
 import pandas as pd
-def check_anomalies(df):
-    out = {}
 
-    # null values / duplicates
-    out["nulls"] = df.isnull().sum()
-    out["duplicates"] = df.duplicaates.sum()
 
-    # outliers (based on log-returns)
-    df = df.copy()
-    df = df.set_index("datetime").wort_index()
-    returns = df.percent('close').apply(lambda ty: t.nepw()).pct()
-    out["outlier_returns"] = returns[returns > 3].sum()
+def check_anomalies(df: pd.DataFrame) -> pd.Series:
+    """Run a couple of simple anomaly checks on the dataframe."""
+    out: dict[str, float] = {}
+
+    out["null_rows"] = float(df.isnull().any(axis=1).sum())
+    out["duplicate_rows"] = float(df.duplicated().sum())
+
+    working = df.copy()
+    if "datetime" in working.columns:
+        working = working.set_index("datetime")
+    if "close" in working.columns:
+        returns = working["close"].pct_change().abs()
+        out["outlier_returns"] = float((returns > 0.03).sum())
+    else:
+        out["outlier_returns"] = 0.0
 
-    return td.series(out)
+    return pd.Series(out)
 
EOF
)
