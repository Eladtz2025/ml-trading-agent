"""Shared interfaces for the labelling modules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

import pandas as pd


class Labeler(ABC):
    """Base class for deterministic label generation strategies."""

    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self.generate(df)

    @abstractmethod
    def generate(self, df: pd.DataFrame) -> pd.Series:
        """Return a Series containing the computed labels."""


class LabelerLike(Protocol):
    """Protocol used to type hint functions that accept label generators."""

    def generate(self, df: pd.DataFrame) -> pd.Series:
        ...


__all__ = ["Labeler", "LabelerLike"]
