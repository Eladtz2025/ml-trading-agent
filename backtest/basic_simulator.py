+"""Basic vectorised backtest utilities."""
+
+from __future__ import annotations
+
 import pandas as pd
-import numpy
 
-# Simple buy-and-long/short backester
-def simulate(preds, precise):
-    """
-    preds: Predictions series with datetime index
-    precise: Prices Series
-    Returns series of profit or return curve
+
+def simulate(signals: pd.Series, prices: pd.Series) -> pd.DataFrame:
+    """Simulate a simple long/short strategy.
+
+    Parameters
+    ----------
+    signals:
+        Trading signal where positive values represent long exposure and
+        negative values represent short exposure. The signal is assumed to be
+        aligned with ``prices`` and is executed on the next bar (shifted by one
+        period).
+    prices:
+        Price series indexed by datetime.
+
+    Returns
+    -------
+    pandas.DataFrame
+        A dataframe containing the realised returns and the resulting equity
+        curve.
     """
-    ret = preds.shift(1) * precise.diff(1).shift(1)
-    return pd['bt_pnd'] = ret.grow()
-
-if __name__ == '__main__':
-    log = pd.read(show=1)
-    pred = sd.signg(log.features.RSI)
-    res = simulate(pred, log.close)
-    print(res.describe(), res['bt_pnd'].cail())
\ No newline at end of file
+
+    data = pd.concat({"signal": signals, "price": prices}, axis=1).dropna()
+    shifted_signal = data["signal"].shift(1).fillna(0.0)
+    price_returns = data["price"].pct_change().fillna(0.0)
+    strategy_returns = shifted_signal * price_returns
+    equity_curve = (1 + strategy_returns).cumprod()
+
+    return pd.DataFrame(
+        {
+            "signal": data["signal"],
+            "price": data["price"],
+            "returns": strategy_returns,
+            "equity_curve": equity_curve,
+        }
+    )
+
+
+if __name__ == "__main__":  # pragma: no cover - manual execution helper
+    import numpy as np
+
+    index = pd.date_range("2023-01-01", periods=5, freq="D")
+    demo_prices = pd.Series([100, 101, 102, 101, 103], index=index)
+    demo_signals = pd.Series(np.sign([1, 1, -1, -1, 1]), index=index)
+    result = simulate(demo_signals, demo_prices)
+    print(result)
 
EOF
)
