"""High level orchestration for the classic training pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml

from backtest.run import run_backtest
from data.get_data_yahoo import fetch_data
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.xgb import XGBModel
from reports.generate import generate_report


def _load_config(path: str | Path) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    if "close" not in frame.columns and "Close" in frame.columns:
        frame["close"] = frame["Close"]
    frame["returns"] = frame["close"].pct_change().fillna(0)
    frame["rsi"] = compute_rsi(frame["close"], window=14)
    return frame.dropna().copy()


def _resolve_report_dir(config: Dict[str, Any]) -> Path:
    report_conf = config.get("report", {})
    path = report_conf.get("path")
    if not path:
        path = config.get("paths", {}).get("artifacts", "artifacts")
    return Path(path)


def run_classic_pipeline(config_path: str | Path) -> Dict[str, Any]:
    config = _load_config(config_path)

    data_conf = config.get("data", {})
    symbol = data_conf.get("symbol", "SPY")
    start = data_conf.get("start", "2020-01-01")
    end = data_conf.get("end", "2023-01-01")

    raw = fetch_data(symbol, start, end)
    features = _prepare_features(raw)
    labels_raw = label_next_bar(features["close"]).reindex(features.index).fillna(0)
    labels = (labels_raw > 0).astype(int)

    model_conf = config.get("models", {}).get("params", {})
    model = XGBModel(params=model_conf)
    summary, predictions = run_backtest(features[["returns", "rsi"]], labels, model)

    report_payload = {
        "quotes": features["close"],
        "metrics": summary,
        "predictions": predictions,
        "config": config,
    }

    output_dir = _resolve_report_dir(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    generate_report(report_payload, output_dir)

    return report_payload
