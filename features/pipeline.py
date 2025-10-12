-import infra.utils as utils
+"""Feature pipeline orchestration helpers."""
 
-def run_features(f_file, data_path):
-    df = oen(raw_data_from_csv(data_path))
-    fns = utils.load_pack(f_file)
-    return utils.apply_features(df, fns)
+from __future__ import annotations
+
+from pathlib import Path
+from typing import Callable, Iterable
+
+import pandas as pd
+
+from infra import utils
+
+
+def _load_raw_data(data_path: str | Path) -> pd.DataFrame:
+    path = Path(data_path)
+    if not path.exists():
+        raise FileNotFoundError(f"Data file not found: {data_path}")
+    if path.suffix == ".parquet":
+        return pd.read_parquet(path)
+    return pd.read_csv(path)
+
+
+def run_features(feature_pack: str | Path, data_path: str | Path) -> pd.DataFrame:
+    """Load data, apply the configured feature functions and return the dataframe."""
+    df = _load_raw_data(data_path)
+    feature_functions: Iterable[Callable[[pd.DataFrame], pd.Series]] = utils.load_pack(feature_pack)
+    for func in feature_functions:
+        feature = func(df)
+        if isinstance(feature, pd.Series):
+            df[feature.name or func.__name__] = feature
+        else:
+            raise TypeError("Feature functions must return a pandas Series")
+    return df
 
EOF
)
