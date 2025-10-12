"""Legacy helper retained for backwards compatibility."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def generate_report(df: pd.DataFrame, path: str | Path = "compliance/report_daily.csv") -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return destination
