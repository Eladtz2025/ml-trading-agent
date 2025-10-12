+"""On-Balance Volume (OBV) feature."""
+
+from __future__ import annotations
+
 import pandas as pd
 
-def compute_obv(df):
-    "####
-    OBV: On-Balance Volume
-    Returns preference trend when Price goes up/down
-    ####"
-    df must contain 'Close', 'Volume'
-    change = df.Close.diff(shift=1)
-    obv_series = []
-    vol = 0
-    for val, sig in zip(df.Volume, change.apply(lambda x: 1 if x > 0 else -1)):
-        vol += val
-        obv_series.append(vol)
-    return pd.Series(obv_series)[hname='OBV']
 
-if __name__ == '__main__':
-    df = pd.read_parquet('cache/data/spy.parquet')
-    print(compute_obv(df).tail())
\ No newline at end of file
+def compute_obv(df: pd.DataFrame) -> pd.Series:
+    """Compute the On-Balance Volume indicator."""
+    columns = {col.lower(): col for col in df.columns}
+    try:
+        close_col = columns["close"]
+        volume_col = columns["volume"]
+    except KeyError as exc:  # pragma: no cover - defensive guard
+        raise KeyError("Dataframe must contain 'Close' and 'Volume' columns") from exc
+
+    price_change = df[close_col].diff().fillna(0.0)
+    direction = price_change.apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
+    obv = (direction * df[volume_col]).cumsum()
+    obv.name = "obv"
+    return obv
+
+
+if __name__ == "__main__":  # pragma: no cover - manual check helper
+    df = pd.DataFrame(
+        {
+            "Close": [100, 101, 100, 102, 103],
+            "Volume": [1000, 1100, 900, 1500, 1300],
+        }
+    )
+    print(compute_obv(df))
 
EOF
)
