+"""Volume Weighted Average Price feature."""
+
+from __future__ import annotations
+
 import pandas as pd
 
-def compute_vwap(df):
-    """
-    Compute cumulative Vwap: close weighted by volume
-     df must contain 'Close', 'Volume'
-    vp = (df.Close * df.Volume).cumsum()
-    cumv_vol = df.Volume.cumsum()
-    return vp/ cumv_vol
-
-# if __name__ == '__main__':
-    import pdf
-    df = pdf.read_parquet('cache/data/spy.parquet')
-    print(compute_wvap(df).tail())
\ No newline at end of file
+
+def compute_vwap(df: pd.DataFrame) -> pd.Series:
+    """Compute the cumulative VWAP for a dataframe."""
+    columns = {col.lower(): col for col in df.columns}
+    try:
+        close_col = columns["close"]
+        volume_col = columns["volume"]
+    except KeyError as exc:
+        raise KeyError("Dataframe must contain 'Close' and 'Volume' columns") from exc
+
+    value = (df[close_col] * df[volume_col]).cumsum()
+    volume = df[volume_col].cumsum()
+    vwap = (value / volume).rename("vwap")
+    return vwap
+
+
+if __name__ == "__main__":  # pragma: no cover - quick check helper
+    df = pd.DataFrame(
+        {
+            "Close": [100, 102, 101, 103],
+            "Volume": [200, 180, 220, 210],
+        }
+    )
+    print(compute_vwap(df))
 
EOF
)
