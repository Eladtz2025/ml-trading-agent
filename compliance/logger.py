"""Utility helpers for compliance logging."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

DECISION_FILE = Path(__file__).parent / "data" / "decisions.tsv"
COLUMNS = ("date", "signal", "size")


def log_decisions(date: str, signal: int, size: int) -> None:
    """Append a trading decision to the compliance log."""
    DECISION_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = pd.DataFrame([(date, signal, size)], columns=COLUMNS)
    mode = "a" if DECISION_FILE.exists() else "w"
    header = not DECISION_FILE.exists()
    record.to_csv(DECISION_FILE, sep="\t", index=False, mode=mode, header=header)


def load_decisions(columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Load the compliance decision log."""
    if not DECISION_FILE.exists():
        return pd.DataFrame(columns=list(columns) if columns is not None else COLUMNS)

    df = pd.read_csv(DECISION_FILE, sep="\t")
    if columns is not None:
        missing = set(columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns in decision log: {missing}")
        df = df[list(columns)]
    return df
