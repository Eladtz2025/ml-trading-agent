"""Utilities for detecting population drift using the Population Stability Index."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

DEFAULT_THRESHOLD = 0.1


def load_current_features(path: str | Path) -> pd.DataFrame:
    """Load a dataframe of current features from ``path``."""

    frame_path = Path(path)
    if not frame_path.exists():
        raise FileNotFoundError(f"Current feature file not found: {frame_path}")
    if frame_path.suffix == ".parquet":
        return pd.read_parquet(frame_path)
    return pd.read_csv(frame_path)


def load_reference_features(model_path: str | Path) -> pd.DataFrame:
    """Load reference features associated with ``model_path``."""

    reference_path = Path(model_path).with_suffix(".features.parquet")
    if reference_path.exists():
        return pd.read_parquet(reference_path)
    raise FileNotFoundError(
        "Reference features not found. Expected to locate "
        f"{reference_path}. Provide a cached reference dataset."
    )


def psi_drift(
    current: pd.DataFrame,
    reference: pd.DataFrame,
    threshold: float = DEFAULT_THRESHOLD,
) -> Dict[str, float]:
    """Calculate the PSI for overlapping columns between two datasets."""

    deltas: Dict[str, float] = {}
    shared_cols = [col for col in current.columns if col in reference.columns]
    if not shared_cols:
        return deltas

    for column in shared_cols:
        current_col = current[column].dropna()
        reference_col = reference[column].dropna()
        if current_col.empty or reference_col.empty:
            continue

        combined = pd.concat([current_col, reference_col])
        bins = np.linspace(combined.min(), combined.max(), num=11)
        if np.allclose(bins[0], bins[-1]):
            continue

        observed, _ = np.histogram(current_col, bins=bins)
        expected, _ = np.histogram(reference_col, bins=bins)

        observed = observed / max(observed.sum(), 1)
        expected = expected / max(expected.sum(), 1)

        mask = (observed > 0) & (expected > 0)
        if not mask.any():
            continue

        psi = float(
            ((observed[mask] - expected[mask]) * np.log(observed[mask] / expected[mask])).sum()
        )

        if psi > threshold:
            deltas[column] = psi

    return deltas


__all__ = [
    "DEFAULT_THRESHOLD",
    "load_current_features",
    "load_reference_features",
    "psi_drift",
]
