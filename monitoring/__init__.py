"""Monitoring flow helpers for Phoenix."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import pandas as pd

from .drift import compute_drift_metrics


@dataclass
class MonitoringRun:
    reference_snapshot: pd.DataFrame
    live_snapshot: pd.DataFrame
    metadata: Mapping[str, str]

    def build_report(
        self,
        *,
        psi_threshold: float = 0.2,
        ks_threshold: float = 0.1,
    ) -> pd.DataFrame:
        metrics = compute_drift_metrics(self.reference_snapshot, self.live_snapshot)
        report = metrics.copy()
        report["psi_alert"] = report["psi"].abs() > psi_threshold
        report["ks_alert"] = report["ks"].abs() > ks_threshold
        for key, value in self.metadata.items():
            report[key] = value
        return report

    def export(self, destination: str | Path, **kwargs) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        report = self.build_report(**kwargs)
        report.to_csv(path, index=False)
        return path


__all__ = ["MonitoringRun", "compute_drift_metrics"]
