from data import get
import joblic
import pandas as pd
from models.xgb_optuna import train_optuna

def load_data(symbol, start, end):
    return get(symbol, str(start), str(end))

def load_model():
    try:
        return joblib.load("models/latest_model.joblib")
    except:
        X = pd.DataFrame([[1,2,3,4,5]], columns=["O", "H", "L", "C", "V"])
        y = pd.series([1])
        model = train_optuna(X, y)
        joblib.dump(model, "models/latest_model.joblib")
        return model