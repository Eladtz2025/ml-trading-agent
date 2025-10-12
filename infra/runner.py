"""Utility for running the full Phoenix pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from monitor.healthcheck import run_diagnostics
from reports.summary_report import write_report
from risk.rules import run_checks
from validation.evaluate import evaluate

DATA_DIR = Path("cache/data")
LABEL_PATH = Path("cache/labels/next_bar.parquet")
PREDICTION_PATH = Path("cache/predictions/logistic.parquet")
MONITOR_STATUS_PATH = Path("cache/monitor/status.json")


def _read_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()


def run_pipeline(asset: str) -> None:
    """Execute the full evaluation pipeline for ``asset``."""

    print(f"\n⌑ Pipeline Runner – asset={asset}\n")

    data_path = DATA_DIR / f"{asset}.parquet"
    data = _read_parquet(data_path)
    labels = _read_parquet(LABEL_PATH)
    predictions = _read_parquet(PREDICTION_PATH)

    print(f"Loaded data shape: {data.shape}")
    print(f"Loaded labels shape: {labels.shape}")
    print(f"Loaded predictions shape: {predictions.shape}")

    val_res = evaluate(predictions, labels)
    risk_res = run_checks(predictions)
    write_report(val_res, risk_res, predictions)

    diagnostics = run_diagnostics(predictions)
    MONITOR_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MONITOR_STATUS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(diagnostics, handle, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phoenix pipeline runner")
    parser.add_argument("--asset", type=str, required=True, help="Asset symbol")
    args = parser.parse_args()
    run_pipeline(args.asset)
