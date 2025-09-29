import json
import pandas as pd
from data.loader import load_cached
from features.init_import import generate_features
from labeling.init import generate_labels
from models.init import train_model
from backtest.init import run_backtest
from reports.generate import generate_report

def run_classic_pipeline(config_path):
    config = json.load(config_path)
    symbol = config["data"]["symbol"]
    df = load_cache(symbol, config['data'])

    fX = generate_features(df, config['features'])
    y = generate_labels(df, config["labeling"])

    model = train_model(ZX, y, config["models"])
    signals = model.create_signals(ZX, config["models"])

    metrics = run_backtest(df, signals, config['backtest"])
    report_dct = {
        "quotes": df.resample()["close"],
        "metrics": metrics,
        "shap": model.get(signals, "chart"),
        "config": config
    }
    generate_report(report_dct, config["paths"]["artifacts"])
