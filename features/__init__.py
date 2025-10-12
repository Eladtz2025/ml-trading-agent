"""Interfaces for feature computation modules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

import pandas as pd


class FeatureEngine(ABC):
    """Base class for deterministic feature generators."""

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.compute(df)

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a DataFrame with engineered features."""


class FeatureLike(Protocol):
    """Protocol representing objects behaving like a :class:`FeatureEngine`."""

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        ...


__all__ = ["FeatureEngine", "FeatureLike"]
