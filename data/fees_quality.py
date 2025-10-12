"""Fee quality validation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import pandas as pd


@dataclass
class FeeQualityReport:
    """Summary statistics describing potential data issues in fee series."""

    total_records: int
    negative_fees: int
    extreme_spikes: int
    missing_values: int

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "total_records": [self.total_records],
                "negative_fees": [self.negative_fees],
                "extreme_spikes": [self.extreme_spikes],
                "missing_values": [self.missing_values],
            }
        )


@dataclass
class FeeQualityOutcome:
    """Container holding summary statistics and anomaly mask."""

    report: FeeQualityReport
    anomalies: pd.Series

    def to_frame(self) -> pd.DataFrame:
        """Return a dataframe combining the report with anomaly counts."""

        frame = self.report.to_frame().copy()
        frame["anomaly_count"] = int(self.anomalies.sum())
        return frame


def _detect_extreme_spikes(series: pd.Series, threshold: float = 5.0) -> int:
    returns = series.pct_change(fill_method=None).abs()
    return int((returns > threshold).sum())


def evaluate_fee_quality(df: pd.DataFrame, column: str = "fees") -> FeeQualityReport:
    """Compute high-level quality checks for fee time-series data."""

    if column not in df.columns:
        raise KeyError(f"'{column}' column is required for fee quality evaluation")

    fees = df[column].astype(float)
    return FeeQualityReport(
        total_records=int(fees.shape[0]),
        negative_fees=int((fees < 0).sum()),
        extreme_spikes=_detect_extreme_spikes(fees),
        missing_values=int(fees.isna().sum()),
    )


def export_fee_quality(
    report: FeeQualityReport,
    destination: str | Path,
    metadata: Mapping[str, str] | None = None,
) -> Path:
    """Persist the fee quality report with optional metadata annotations."""

    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    payload = report.to_frame()
    if metadata:
        for key, value in metadata.items():
            payload[key] = value

    payload.to_csv(destination_path, index=False)
    return destination_path


def detect_fee_anomalies(df: pd.DataFrame, column: str = "fees", z_threshold: float = 4.0) -> pd.Series:
    """Return boolean mask of anomalous fee changes using a percent-change threshold."""

    if column not in df.columns:
        raise KeyError(f"'{column}' column is required for anomaly detection")

    fees = df[column].astype(float)
    pct_changes = fees.pct_change(fill_method=None).fillna(0.0).abs()
    mask = pct_changes > z_threshold
    return pd.Series(mask, index=df.index, name="fee_anomaly")


def validate_fee_history(
    df: pd.DataFrame,
    *,
    column: str = "fees",
    z_threshold: float = 4.0,
) -> FeeQualityOutcome:
    """Run fee quality evaluation and anomaly detection in a single call."""

    report = evaluate_fee_quality(df, column=column)
    anomalies = detect_fee_anomalies(df, column=column, z_threshold=z_threshold)
    return FeeQualityOutcome(report=report, anomalies=anomalies)
