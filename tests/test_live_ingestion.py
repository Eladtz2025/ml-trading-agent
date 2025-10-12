"""Tests for the live data ingestion manager."""

from __future__ import annotations

from pathlib import Path

import pytest

from data.live import LiveIngestionManager, StreamTag


def test_register_and_ingest(tmp_path: Path) -> None:
    manager = LiveIngestionManager(root=tmp_path)
    manager.register_tag(
        StreamTag(
            name="synthetic_prices",
            description="Synthetic quote stream",
            schema={"symbol": "string", "price": "float"},
        )
    )

    destination = manager.ingest_records(
        "synthetic_prices",
        [
            {"symbol": "TEST", "price": 100.0},
            {"symbol": "TEST", "price": 101.5},
        ],
    )

    assert destination.exists()
    frame = manager.load_live_frame("synthetic_prices")
    assert len(frame) == 2
    assert set(frame.columns) == {"symbol", "price", "ingested_at"}


def test_missing_tag_raises(tmp_path: Path) -> None:
    manager = LiveIngestionManager(root=tmp_path)
    with pytest.raises(KeyError):
        manager.ingest_records("unknown", [{"foo": 1}])
