"""Integration tests for the monitoring flow."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from monitoring import MonitoringRun


def test_monitoring_run_exports_report(tmp_path: Path) -> None:
    reference = pd.DataFrame({"feature": [0, 0, 0], "extra": [1, 2, 3]})
    live = pd.DataFrame({"feature": [1, 1, 1], "extra": [3, 2, 1]})

    run = MonitoringRun(reference, live, metadata={"run_id": "abc"})
    path = run.export(tmp_path / "report.csv")

    assert path.exists()
    frame = pd.read_csv(path)
    assert "run_id" in frame.columns
