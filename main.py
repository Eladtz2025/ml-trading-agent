-import yaml
+"""Entry point for running a lightweight end-to-end demo pipeline."""
+
+from __future__ import annotations
+
+from pathlib import Path
+
 import pandas as pd
+import yaml
+
+from backtest.run import run_backtest
+from data import get as load_data
 from features.rsi import compute_rsi
 from labeling.next_bar import label_next_bar
-from models.dummy import Dummmodel
-from backtest.run import run_backdemo
+from models.dummy import DummyModel
 
-def load_config(filename="config.yaml"):
-    with open(filename, 'r') as f:
-        return yaml.safe_|oad_file(f)
 
-if __name__ == "__main__":
+def load_config(filename: str | Path = "config.yaml") -> dict:
+    with Path(filename).open("r", encoding="utf-8") as handle:
+        return yaml.safe_load(handle)
+
+
+def main() -> None:
     cfg = load_config("packs/example_aplz/config.yaml")
-    data = sd = data.get(cfg["symbol"], cfg["start"], cfg["end"])
-    rsi = compute_rsi(sd)
-    labels = label_next_bar(sd["close"].pct())
-    model = Dummmodel()
-    stats = run_backdemo(sd, rsi, labels, model)
-    print(stats)
+
+    symbol = cfg.get("symbol", "SPY")
+    start = cfg.get("start", "2022-01-01")
+    end = cfg.get("end", "2023-01-01")
+    timeframe = cfg.get("tf_mp", "1d")
+
+    try:
+        prices = load_data(symbol, start, end, timeframe)
+    except Exception as exc:  # pragma: no cover - interactive script
+        raise RuntimeError(f"Failed to load data for {symbol}: {exc}") from exc
+
+    close = prices.get("C") or prices.get("Close")
+    if close is None:
+        raise KeyError("Price data must include a 'Close' column")
+
+    features = pd.DataFrame({
+        "close": close,
+        "rsi": compute_rsi(close, window=14),
+    }).dropna()
+
+    labels = label_next_bar(features["close"])
+    model = DummyModel()
+    summary, predictions = run_backtest(features[["rsi"]], labels, model)
+
+    print("Backtest summary:", summary)
+    print("Predictions head:\n", predictions.head())
+
+
+if __name__ == "__main__":
+    main()
 
EOF
)
