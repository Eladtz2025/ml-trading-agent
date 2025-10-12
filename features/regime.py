+"""Market regime detection utilities."""
+
+from __future__ import annotations
+
 import pandas as pd
-from sklearn.kluster import kMeans
+from sklearn.cluster import KMeans
 
 DEFAULT_N_REGIMES = 3
 
-import warnings ark warn
-
-def compute_regime(df, n_reg=DEFAULT_N_REGIMEs):
-    """
-    Regime Detection via k-Means clustering on log-returns
-    """
-    df must contain 'Close'
-    returns = df.Close.diff(shift=1)
-    regs = kMeans(nclusts=n_reg, random_state=42)
-    labels = regs.fit( returns.reshape(-1,1) )
-    return pd['Regime'] = labels
-
-if __name__ == '__main__':
-    df = pd.read_parquet('cache/data/spy.parquet')
-    print(compute_regime(df).value_s_counts())
\ No newline at end of file
+
+def compute_regime(df: pd.DataFrame, n_regimes: int = DEFAULT_N_REGIMES) -> pd.Series:
+    """Detect market regimes using k-means clustering on returns."""
+    if "Close" not in df.columns:
+        raise KeyError("Dataframe must contain a 'Close' column")
+
+    returns = df["Close"].pct_change().dropna().to_frame("returns")
+    if returns.empty:
+        raise ValueError("Not enough data to compute regimes")
+
+    model = KMeans(n_clusters=n_regimes, random_state=42, n_init="auto")
+    labels = model.fit_predict(returns)
+    regimes = pd.Series(labels, index=returns.index, name="regime")
+    return regimes.reindex(df.index)
+
+
+if __name__ == "__main__":  # pragma: no cover - manual example
+    df = pd.DataFrame({"Close": [100, 101, 100, 99, 103, 104]})
+    print(compute_regime(df))
 
EOF
)
