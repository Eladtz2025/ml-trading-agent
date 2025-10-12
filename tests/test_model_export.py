"""Tests covering model output and metadata export helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from models import model_io
from models.output import export_predictions


class DummyModel:
    def predict(self, data):
        return data


def test_save_model_writes_metadata(tmp_path: Path) -> None:
    version = model_io.save_model(DummyModel(), tmp_path, config={"alpha": 0.1})
    metadata_path = tmp_path / f"model_{version}.json"

    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert payload["config"] == {"alpha": 0.1}
    assert payload["version_id"] == version
    assert "saved_at" in payload
    assert "git_revision" in payload


def test_export_predictions_saves_signals_and_returns(tmp_path: Path) -> None:
    signals = pd.Series([0.1, -0.2, 0.05], name="signal")
    returns = pd.Series([0.01, -0.02, 0.03], name="returns")

    export_predictions(
        signals,
        returns,
        directory=tmp_path,
        run_id="test_run",
        metadata={"model_version": "abc123"},
    )

    parquet_path = tmp_path / "test_run.parquet"
    meta_path = tmp_path / "test_run.metadata.json"

    assert parquet_path.exists()
    assert meta_path.exists()

    frame = pd.read_parquet(parquet_path)
    assert list(frame.columns) == ["signal", "returns"]

    payload = json.loads(meta_path.read_text(encoding="utf-8"))
    assert payload["metadata"]["model_version"] == "abc123"
