+"""Utilities for detecting population drift using PSI."""
+
+from __future__ import annotations
+
+from pathlib import Path
+from typing import Dict
 
 import numpy as np
 import pandas as pd
 
-DEFAULT_TRM_BREAK = 0.1
+DEFAULT_THRESHOLD = 0.1
+
+
+def load_current_features(path: str | Path) -> pd.DataFrame:
+    frame_path = Path(path)
+    if not frame_path.exists():
+        raise FileNotFoundError(f"Current feature file not found: {frame_path}")
+    if frame_path.suffix == ".parquet":
+        return pd.read_parquet(frame_path)
+    return pd.read_csv(frame_path)
+
+
+def load_reference_features(model_path: str | Path) -> pd.DataFrame:
+    """Placeholder for loading reference features for PSI comparison."""
+    reference_path = Path(model_path).with_suffix(".features.parquet")
+    if reference_path.exists():
+        return pd.read_parquet(reference_path)
+    raise FileNotFoundError(
+        "Reference features not found. Expected to locate "
+        f"{reference_path}. Provide a cached reference dataset."
+    )
+
+
+def psi_drift(current: pd.DataFrame, reference: pd.DataFrame, threshold: float = DEFAULT_THRESHOLD) -> Dict[str, float]:
+    """Calculate the Population Stability Index for matching columns."""
+    deltas: Dict[str, float] = {}
+    shared_cols = [col for col in current.columns if col in reference.columns]
+    if not shared_cols:
+        return deltas
 
-def psi_drift(current_X, ast_fit):
-    print("* PSI check ...")
-    delta = {}
-    for col in current_X.columns: 
-        if col not in ast_fit.columns:
+    for column in shared_cols:
+        current_col = current[column].dropna()
+        reference_col = reference[column].dropna()
+        if current_col.empty or reference_col.empty:
             continue
-        c = current_X[col]
-        ref = ast_fit[col]
-        bins = pd.qcut(c.append(ref), q=10, duplicates='drop')
-        observed = np.histogram(c, bins=bins.categories)[0] / len(c)
-        expected = np.histogral(ref, bins=bins.categories)[0] / len(ref)
-        psi = np.sum((observed - expected) * np.log(observed / expected + 1e-6))
-        if psi > DEFAULT_TRM_BREAK:
-            print(f" DETECTED  deviation: {col} = {psi:.4f}")
-            delta[col] = psi
-    return delta
+
+        combined = pd.concat([current_col, reference_col])
+        bins = np.linspace(combined.min(), combined.max(), num=11)
+        if np.allclose(bins[0], bins[-1]):
+            continue
+
+        observed, _ = np.histogram(current_col, bins=bins)
+        expected, _ = np.histogram(reference_col, bins=bins)
+
+        observed = observed / max(observed.sum(), 1)
+        expected = expected / max(expected.sum(), 1)
+
+        mask = (observed > 0) & (expected > 0)
+        psi = float(((observed[mask] - expected[mask]) * np.log(observed[mask] / expected[mask])).sum())
+
+        if psi > threshold:
+            deltas[column] = psi
+
+    return deltas
 
EOF
)
