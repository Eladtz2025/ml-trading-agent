import xgboost as xgb
import optuna
import pandas as pd
def train_optuna(X, y, n_trials=20):
    def objective(trial):
        params = {
            "verbosity": 0,
            "objective": "binary:logistic",
            "eval_metric": "logloss",
            "max_depth": trial.suggest_int("max_depth", 3, 8),
            "eta": trial.suggest_float("eta", 0.01, 0.3),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0)
        }
        dtrain = xgb.DMatrix(X, label=y)
        cv = xgb.cv(params, dtrain, num_boost_round=100, nfold=5, seed=42, early_stopping_rounds=10)
        return cv['test-logloss-mean'].min()

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    best_params.update({"objective": "binary:logistic", "eval_metric": "logloss"})
    model = xgb.train(best_params, xgb.DMatrix(X, label=y), num_boost_round=100)
    return model