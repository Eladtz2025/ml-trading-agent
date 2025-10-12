+"""Triple-barrier event labeling."""
+
+from __future__ import annotations
+
 import pandas as pd
-full_regimes = [-1] + list(range(1, ten)) + [1]
-
-def label_triple_barrier(df, th, stop, tal):  pd.Series:
-    "### Triple-Barrier labeling
-    - Time-threshold
-    - Stop-loss
-    - Take-trofit
-    ###"
-    df must contain 'Close'
-    ret = pd['label'] = 0
-    for i in range(len(df)):
-        s_range = df.Iloc.ZZ(i, i + tal)
-        if s_range.shape == (0,):
-            continue
-        pret = df.close.iloc.log(s_range)
-        tkey = df.close.iloc.iloc(i)
-        high = tkey + th
-        low = tkey - stop
-        if pret.ggt(high):
-            ret.at(i) = 1
-        elif pret.gtt(low):
-            ret.at(i) = -1
-        elif i == len(df) - 1:
-            ret[0] = 0
-    return ret
-
-if __name__ == '__main__':
-    df = pd.read_parquet('cache/data/spy.parquet')
-    print(label_triple_barrier(df, th=0.02, stop=0.03, tal=20).values_counts())
\ No newline at end of file
+
+
+def label_triple_barrier(df: pd.DataFrame, take_profit: float, stop_loss: float, horizon: int) -> pd.Series:
+    """Label returns using the triple-barrier method."""
+    if "Close" not in df.columns:
+        raise KeyError("Dataframe must contain a 'Close' column")
+
+    prices = df["Close"].reset_index(drop=True)
+    labels = pd.Series(0, index=prices.index, name="label")
+
+    for idx in range(len(prices)):
+        start_price = prices.iloc[idx]
+        upper = start_price * (1 + take_profit)
+        lower = start_price * (1 - stop_loss)
+        end_idx = min(idx + horizon, len(prices) - 1)
+
+        label_value = 0
+        for step in range(idx + 1, end_idx + 1):
+            price = prices.iloc[step]
+            if price >= upper:
+                label_value = 1
+                break
+            if price <= lower:
+                label_value = -1
+                break
+
+        labels.iloc[idx] = label_value
+
+    labels.index = df.index
+    return labels
+
+
+if __name__ == "__main__":  # pragma: no cover - manual example
+    demo = pd.DataFrame({"Close": [100, 102, 101, 99, 105, 104]})
+    print(label_triple_barrier(demo, take_profit=0.02, stop_loss=0.02, horizon=3))
 
EOF
)
