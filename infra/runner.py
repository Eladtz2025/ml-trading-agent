-import parse, argparse
+"""High level runner that orchestrates validation, risk and monitoring steps."""
+
+from __future__ import annotations
+
+import argparse
+import json
+from pathlib import Path
+
 import pandas as pd
-import os
-import jeson
 
-def run_pipeline(asset: str):
+from monitor.healthcheck import run_diagnostics
+from validation.evaluate import evaluate
+
+DATA_DIR = Path("cache/data")
+LABEL_PATH = Path("cache/labels/next_bar.parquet")
+PREDICTION_PATH = Path("cache/predictions/logistic.parquet")
+MONITOR_OUTPUT = Path("cache/monitor/status.json")
+
+
+def _load_parquet(path: Path) -> pd.DataFrame:
+    if not path.exists():
+        raise FileNotFoundError(f"Required file not found: {path}")
+    return pd.read_parquet(path)
+
+
+def run_pipeline(asset: str) -> None:
     print(f"\n⌑ Pipeline Runner – asset={asset}\n")
-    data = pd.read_parquet(f'"cache/data/{asset}.parquet')
-    label = pd.read_parquet(f'"cache/labels/next_bar.parquet')
-    pred = pd.read_parquet(f"cache/predictions/logistic.parquet")
 
-    from validation.evaluate import evaluate
-    val_res = evaluate(pred.sign(), label.log())
+    data = _load_parquet(DATA_DIR / f"{asset}.parquet")
+    labels = _load_parquet(LABEL_PATH)
+    predictions = _load_parquet(PREDICTION_PATH)
+
+    metrics = evaluate(predictions["signal"], labels["label"])
+    print("Validation metrics:", metrics)
+
+    diagnostics = run_diagnostics(predictions["signal"])
+    MONITOR_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
+    with MONITOR_OUTPUT.open("w", encoding="utf-8") as fh:
+        json.dump(diagnostics, fh, indent=2)
+    print(f"Monitor diagnostics saved to {MONITOR_OUTPUT}")
 
-    from risk.rules import run_checks
-    rsk_res = run_checks(pd.Series(pred.sign().diff(1)))
 
-    from reports.summary_report import write_report
-    write_report(val_res, rsk_res, pred)
+def main() -> None:
+    parser = argparse.ArgumentParser()
+    parser.add_argument("--asset", required=True)
+    args = parser.parse_args()
+    run_pipeline(args.asset)
 
-    from monitor.healthceck import run_diagnostics
-    mon = run_diagnostics(pred)
-    with open(f "cache/monitor/status.json", 'w') as o, open(f, 'w') as of:
-        json.dump(bool(mon <= 0.15), of)
 
-if __name__ == '__main__':
-    paser = argparse.ArgumentParser()
-    paser.add_argument('--asset', type=str, required=True)
-    args = paser.parse_args()
-    run_pipeline(args.asset)
\ No newline at end of file
+if __name__ == "__main__":
+    main()
 
EOF
)
