import numpy as np
import pytest
from sklearn.datasets import make_classification

pytest.importorskip("lightgbm")

from models.mlp_stacking import StackedModelCPU


def test_stacked_model_cpu_fit_predict():
    X, y = make_classification(
        n_samples=120,
        n_features=6,
        n_informative=4,
        random_state=7,
    )

    model = StackedModelCPU(hidden_dim=8, lgbm_params={"n_estimators": 10, "learning_rate": 0.1})
    model.fit(X, y)

    probs = model.predict_proba(X[:5])
    assert probs.shape == (5,)
    assert np.all((0.0 <= probs) & (probs <= 1.0))
