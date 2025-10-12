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
            kind="synthetic",
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
    assert set(frame.columns) == {
        "symbol",
        "price",
        "ingested_at",
        "stream_tag",
        "stream_kind",
        "ingest_mode",
    }
    assert frame["stream_kind"].iloc[0] == "synthetic"
    assert frame["ingest_mode"].unique().tolist() == ["research"]


def test_missing_tag_raises(tmp_path: Path) -> None:
    manager = LiveIngestionManager(root=tmp_path)
    with pytest.raises(KeyError):
        manager.ingest_records("unknown", [{"foo": 1}])


def test_live_mode_appends_mode_column(tmp_path: Path) -> None:
    manager = LiveIngestionManager(root=tmp_path)
    manager.register_tag(
        StreamTag(
            name="equities",
            description="Live equities stream",
            schema={"symbol": "string", "price": "float"},
        )
    )
    manager.set_mode("live")

    manager.ingest_records(
        "equities",
        [
            {"symbol": "XYZ", "price": 10.0},
        ],
    )

    frame = manager.load_live_frame("equities")
    assert frame["ingest_mode"].iloc[-1] == "live"
