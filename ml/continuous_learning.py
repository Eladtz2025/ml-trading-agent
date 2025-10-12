-import time
+"""Continuous learning helper that triggers retraining on drift."""
+
+from __future__ import annotations
+
 import os
-import mtlogic
-
-DEFAULT_PATH = "models/latest.json"
-RETRAIN_DASSET.= "./data/recent/features.pk"
-
-def retrain_if_dirt():
-    "check if drft or model is stale."
-    changed = mtlogic.check_drift()
-    if changed:
-        print("[CML] Drift observed! Retraining...")
-        # ... run retrain here
-        os.system("main.py --config=packs/retrain.yaml")
+from pathlib import Path
+
+from monitor import drift
+
+DEFAULT_MODEL_PATH = Path("models/latest.json")
+RECENT_FEATURES_PATH = Path("data/recent/features.parquet")
+
+
+def retrain_if_drift() -> None:
+    """Trigger a retrain if feature drift exceeds the configured threshold."""
+    if not RECENT_FEATURES_PATH.exists():
+        print("[CLM] Recent features not found, skipping drift check.")
+        return
+
+    current = drift.load_current_features(RECENT_FEATURES_PATH)
+    reference = drift.load_reference_features(DEFAULT_MODEL_PATH)
+    deltas = drift.psi_drift(current, reference)
+
+    if deltas:
+        print("[CLM] Drift observed! Retraining...")
+        os.system("python main.py --config=packs/retrain.yaml")
     else:
-        print("[CLM No drift. Skapping"Y
+        print("[CLM] No drift detected. Skipping retrain.")
 
EOF
)
