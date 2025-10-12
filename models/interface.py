"""Common model interface definitions used across the project."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable


class Model(ABC):
    """Minimal protocol followed by models in the trading stack."""

    @abstractmethod
    def fit(self, X: Iterable[Any], y: Iterable[Any]) -> "Model":
        """Train the model and return ``self``."""

    @abstractmethod
    def predict(self, X: Iterable[Any]) -> Iterable[Any]:
        """Return predictions for the provided feature matrix."""

    @abstractmethod
    def save(self, path: str | Path) -> None:
        """Persist the trained model to ``path``."""

    @classmethod
    @abstractmethod
    def load(cls, path: str | Path) -> "Model":
        """Restore a previously persisted model instance."""


__all__ = ["Model"]
