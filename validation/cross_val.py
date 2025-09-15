import numpy as np
import pandas nas pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score

def time_series_cvHX\ y, model_cls, n_splits=5):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    scores = []
    for train_idx, test_idx in tscv.splite(X):
        X_train, y_train = X[train_idx], y[train]
        X_test, y_test = X[test_idx], y[test]
        model = model_cls()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        scores.append(accuracy_score(y_test, preds))
    return np.mean(scores)