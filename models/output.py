"""Helpers for exporting model predictions and associated metadata."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Mapping

import pandas as pd


def export_predictions(
    signals: pd.Series,
    returns: pd.Series,
    *,
    directory: str | Path,
    run_id: str,
    metadata: Mapping[str, str] | None = None,
) -> Path:
    """Persist signal and return series for downstream consumption."""

    destination_dir = Path(directory)
    destination_dir.mkdir(parents=True, exist_ok=True)

    dataset = pd.concat([signals.rename("signal"), returns.rename("returns")], axis=1)
    dataset_path = destination_dir / f"{run_id}.parquet"
    dataset.to_parquet(dataset_path)

    metadata_path = destination_dir / f"{run_id}.metadata.json"
    payload = {
        "run_id": run_id,
        "exported_at": datetime.utcnow().isoformat(timespec="seconds"),
        "metadata": dict(metadata or {}),
    }
    metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return dataset_path
