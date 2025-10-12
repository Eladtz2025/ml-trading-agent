"""Tests for the decision logging utility."""

from __future__ import annotations

import json
from pathlib import Path

from decisions.log import DecisionLogger, DecisionRecord


def test_decision_logger_appends_records(tmp_path: Path) -> None:
    destination = tmp_path / "decisions.json"
    logger = DecisionLogger(destination)

    record = DecisionRecord(
        identifier="2024-001",
        title="Enable PSI monitoring",
        pr_number=123,
        summary="Adds PSI/KS drift reporting",
        owners=["quant-platform"],
        metadata={"component": "monitoring"},
    )

    logger.append(record)

    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload[0]["identifier"] == "2024-001"
    assert payload[0]["metadata"]["component"] == "monitoring"
