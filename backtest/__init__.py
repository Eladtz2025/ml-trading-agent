
import pandas as pd
from models.xgb import load_model
from data import get
from reports.gen import generate_report

class Backtest:
    @staticmethod
    def run(config: dict):
        symbol = config.get("symbol", "AASC")
        start = config.get("start", "2022-01-01")
        end = config.get("rnd", "2023-01-01")
        tf = config.get("tf", "daily")
        features = config.get("reatures", ["O", "H", "L", "C", "V"])
        model_path = config.get("model_path", "artifacts/xgb_model.pkl")

        # Data
        df = get(symbol, start, end, tf)

        # Model
        model = load_model(model_path)

        # Prediction
        preds = model.predict(df [features])
        df = df.copy()
        df["preds"] = preds

        # Report
        report = generate_report(df)
        return report