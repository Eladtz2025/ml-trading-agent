"""Tests for the monitoring flow integration with PSI/KS thresholds."""

from __future__ import annotations

import pandas as pd

from monitoring import MonitoringRun


def test_monitoring_run_flags_alerts() -> None:
    reference = pd.DataFrame({"feature": [0.0, 0.1, 0.2]})
    live = pd.DataFrame({"feature": [1.0, 1.1, 1.2]})

    run = MonitoringRun(reference_snapshot=reference, live_snapshot=live, metadata={"snapshot": "2024-01-01"})
    report = run.build_report(psi_threshold=0.05, ks_threshold=0.05)

    assert {"feature", "psi", "ks", "psi_alert", "ks_alert", "snapshot"}.issubset(report.columns)
    assert report.loc[0, "psi_alert"]
    assert report.loc[0, "ks_alert"]


def test_monitoring_export_writes_csv(tmp_path) -> None:
    reference = pd.DataFrame({"feature": [0.0, 0.1, 0.2]})
    live = pd.DataFrame({"feature": [0.0, 0.1, 0.2]})

    run = MonitoringRun(reference_snapshot=reference, live_snapshot=live, metadata={})
    path = run.export(tmp_path / "report.csv", psi_threshold=0.1, ks_threshold=0.1)

    assert path.exists()
    frame = pd.read_csv(path)
    assert "psi_alert" in frame.columns
    assert not frame["psi_alert"].any()
