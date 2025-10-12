+"""Model evaluation utilities."""
+
+from __future__ import annotations
+
+from typing import Iterable
+
+import numpy as np
 import pandas as pd
 from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
 
-functools = {
-    'sharpe': lambda pr: pr.shape[0] / pr.std()
-}
 
-metrics = ['accuracy', 'precision', 'recall', 'roc_auc']
+_METRICS = {
+    "accuracy": accuracy_score,
+    "precision": precision_score,
+    "recall": recall_score,
+    "roc_auc": roc_auc_score,
+}
 
 
-def evaluate(preds, labels):
-    """Metrics including financial & trading"""
-    res = {}
-    res['ACC'] = accuracy_score(labels, preds)
-    res['PRC'] = precision_score(labels, preds)
-    res['REC'] = recall_score(labels, preds)
-    res['AUC'] = roc_auc_score(labels, preds)
+def _sharpe_ratio(returns: pd.Series) -> float:
+    if returns.std() == 0:
+        return 0.0
+    return float(np.sqrt(252) * returns.mean() / returns.std())
 
-    if 'bt_pnd' in preds:
-        res['SHARPE'] = functools['sharpe'](pd.Series(preds['bt_pnd'].log().diff(1)))
 
-    return res
+def evaluate(preds: Iterable[int], labels: Iterable[int]) -> dict:
+    """Calculate a collection of classification and trading metrics."""
+    y_pred = np.asarray(list(preds))
+    y_true = np.asarray(list(labels))
+    if y_pred.size != y_true.size:
+        raise ValueError("preds and labels must have the same length")
 
+    results = {key.upper(): float(func(y_true, y_pred)) for key, func in _METRICS.items()}
 
-if __name__ == '__main__':
-    df = pd.read_parquet('cache/data/spy.parquet')
-    label = pd.read_parquet('cache/labels/next_bar.parquet')
-    pred = pd.read_parquet('cache/predictions/logistic.parquet')
-    res = evaluate(pred.sign(), label.loc())
-    print(pd.Series(f"\n📊 EVALUATION 新状 \n"))
-    print(res)
+    returns = pd.Series(y_pred).diff().fillna(0)
+    results["SHARPE"] = _sharpe_ratio(returns)
+    return results 
EOF
)
