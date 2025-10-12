"""Data loading utilities for CSV and Parquet artefacts."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def read_csv(path: str | Path, columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Read a CSV file and optionally select a subset of columns."""

    df = pd.read_csv(path)

    if columns is None:
        return df

    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise KeyError(f"Missing columns in {path!s}: {', '.join(missing)}")

    return df.loc[:, list(columns)]


def save_parquet(df: pd.DataFrame, path: str | Path, *, index: str | None = None) -> Path:
    """Persist a DataFrame in Parquet format."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    data = df.copy()
    if index is not None and index in data.columns:
        data = data.set_index(index)

    data.to_parquet(destination)
    return destination
