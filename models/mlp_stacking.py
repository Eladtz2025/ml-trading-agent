import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib, os


class StackedModelCPU:
    """
    Lightweight stacking model combining MLP + LGBM for CPU environments.
    """

    def __init__(self, hidden_dim=16, mlp_lr=0.001, lgbm_params=None):
        self.mlp = MLPClassifier(
            hidden_layer_sizes=(hidden_dim,),
            activation="relu",
            solver="adam",
            learning_rate_init=mlp_lr,
            max_iter=300,
            random_state=42,
        )
        self.lgbm = LGBMClassifier(**(lgbm_params or {"n_estimators": 200, "learning_rate": 0.05}))
        self.models = [self.mlp, self.lgbm]
        self.is_fitted = False

    def fit(self, X, y):
        for model in self.models:
            model.fit(X, y)
        self.is_fitted = True
        return self

    def predict_proba(self, X):
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        probs = [m.predict_proba(X)[:, 1] for m in self.models]
        stacked = np.mean(probs, axis=0)
        return stacked

    def train_and_log(self, X, y):
        print("🚀 Training stacked model (MLP + LGBM) on CPU...")
        self.fit(X, y)
        preds = self.predict_proba(X)
        preds_label = (preds > 0.5).astype(int)
        acc = accuracy_score(y, preds_label)
        ret = pd.Series(preds).pct_change().fillna(0)
        sharpe = np.mean(ret) / np.std(ret) * np.sqrt(252) if np.std(ret) > 0 else 0
        print(f"✅ Done — Accuracy: {acc:.3f} | Sharpe (sim): {sharpe:.2f}")

        os.makedirs("cache/models", exist_ok=True)
        joblib.dump(self, "cache/models/mlp_stacking.pkl")
        print("📦 Model saved → cache/models/mlp_stacking.pkl")


if __name__ == "__main__":
    print("⚙️  StackedModelCPU module ready.")
