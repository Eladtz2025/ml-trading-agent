"""Simple utilities used by the monitoring dashboard."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def run_diagnostics(preds: pd.Series) -> dict:
    """Return a collection of lightweight quality checks for ``preds``."""

    series = preds.astype(float)
    if series.empty:
        return {"count": 0, "missing": 0, "mean": 0.0, "psi_drift": 0.0}

    count = int(series.count())
    missing = int(series.isna().sum())
    mean = float(series.mean())

    shifted = series.shift(1)
    drift = float((series - shifted).abs().mean()) if count > 1 else 0.0

    return {
        "count": count,
        "missing": missing,
        "mean": mean,
        "psi_drift": drift,
    }


def _default_predictions_path() -> Path:
    return Path("cache/predictions/latest.parquet")


def _default_output_path() -> Path:
    return Path("cache/monitor/status.json")


if __name__ == "__main__":  # pragma: no cover
    predictions_path = _default_predictions_path()
    output_path = _default_output_path()

    if not predictions_path.exists():
        raise FileNotFoundError(f"Missing predictions file: {predictions_path!s}")

    predictions = pd.read_parquet(predictions_path)["prediction"]
    diagnostics = run_diagnostics(predictions)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(diagnostics, fh, indent=2)

    print(f"Healthcheck saved to {output_path!s}")
