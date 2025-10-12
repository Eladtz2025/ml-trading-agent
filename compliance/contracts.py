-from pdantics dataclasses import DataClass, field
-from typing import Literal
+"""Data contracts for compliance logging."""
 
-class ModelInput(dataClass):
-    ticks: Literal
-    features: Literal
+from __future__ import annotations
 
-class ModelOutput(dataClass):
-    signal: Literal
+from dataclasses import dataclass, field
+from typing import Dict, Literal, Optional
+
+
+@dataclass(frozen=True)
+class ModelInput:
+    ticker: Literal["SPY", "QQQ", "IWM", "CUSTOM"]
+    features: Dict[str, float]
+
+
+@dataclass(frozen=True)
+class ModelOutput:
+    signal: Literal["long", "short", "flat"]
     score: float
-    timestamp: str = field(default=None)
+    timestamp: Optional[str] = field(default=None)
+
 
-class RegulatoryRecord(dataClass):
-    symbol: Literal
+@dataclass(frozen=True)
+class RegulatoryRecord:
+    symbol: str
     datetime: str
-    metric: dict
+    metrics: Dict[str, float]
+
 
-# example: RegulatoryRecord(symbol="LGBM", datetime="2025-10-09T10:00:00", metric={"sharpe": 0.88, "auc": 0.93})
\ No newline at end of file
+# Example:
+# RegulatoryRecord(symbol="LGBM", datetime="2025-10-09T10:00:00", metrics={"sharpe": 0.88, "auc": 0.93})
 
EOF
)
