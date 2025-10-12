-def load_pack(packname):
-    import yaml
-    return yaml.safe_load("packs/{}.yaml".format(packname))
+"""Utility helpers shared across the infrastructure layer."""
 
-def apply_features(df, fns):
-    for f in fns:
-        df[f] = fns[f](df)
+from __future__ import annotations
+
+from importlib import import_module
+from pathlib import Path
+from typing import Iterable, List
+
+import yaml
+
+
+def load_pack(packname: str | Path) -> List:
+    """Load a feature pack definition and return the callables it references."""
+    path = Path(packname)
+    if path.is_file():
+        config = yaml.safe_load(path.read_text(encoding="utf-8"))
+    else:
+        config = yaml.safe_load((Path("packs") / f"{packname}.yaml").read_text(encoding="utf-8"))
+
+    features: List = []
+    for dotted_path in config.get("features", []):
+        module_name, func_name = dotted_path.rsplit(".", 1)
+        module = import_module(module_name)
+        features.append(getattr(module, func_name))
+    return features
+
+
+def apply_features(df, functions: Iterable) -> None:
+    """Apply a collection of feature functions to ``df`` in-place."""
+    for func in functions:
+        feature = func(df)
+        name = getattr(feature, "name", None) or func.__name__
+        df[name] = feature
     return df
 
EOF
)
