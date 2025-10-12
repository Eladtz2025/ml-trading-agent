import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib
import os


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
