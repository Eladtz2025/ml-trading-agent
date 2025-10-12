"""Helpers for computing label confidence scores."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


def probability_from_returns(returns: pd.Series, threshold: float) -> pd.Series:
    """Convert realised returns into a confidence score between 0 and 1."""

    threshold = float(threshold)
    winsorised = returns.clip(lower=-threshold, upper=threshold)
    scaled = (winsorised + threshold) / (2 * threshold)
    return scaled.fillna(0.5)


@dataclass
class LabelWithConfidence:
    label: int
    confidence: float


def assign_with_threshold(returns: pd.Series, threshold: float) -> pd.DataFrame:
    """Assign labels with optional confidence score based on long-term return threshold."""

    returns = returns.astype(float)
    labels = (returns >= threshold).astype(int) - (returns <= -threshold).astype(int)
    confidence = probability_from_returns(returns, threshold)
    return pd.DataFrame({
        "label": labels,
        "confidence": confidence,
    })
