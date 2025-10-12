"""Base model helpers shared across simple estimators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Mapping


class BaseModel(ABC):
    """Provide lightweight structure for the trading models.

    The class mirrors the familiar scikit-learn flow by exposing ``fit`` and
    ``predict`` methods while allowing subclasses to focus on the actual
    implementation.  We keep a small ``_is_fitted`` flag so consumers can guard
    against accidental usage of an unfitted model.
    """

    def __init__(self) -> None:
        self._is_fitted = False

    def fit(self, X: Iterable[Any], y: Iterable[Any], config: Mapping[str, Any] | None = None) -> "BaseModel":
        """Train the estimator using subclass-provided logic."""

        self._fit(X, y, config or {})
        self._is_fitted = True
        return self

    @abstractmethod
    def _fit(self, X: Iterable[Any], y: Iterable[Any], config: Mapping[str, Any]) -> None:
        """Perform the actual fitting procedure."""

    def predict(self, X: Iterable[Any]):
        """Generate trading signals after ensuring the model is trained."""

        if not self._is_fitted:
            raise RuntimeError("Cannot call predict before the model has been fitted")
        return self._predict(X)

    @abstractmethod
    def _predict(self, X: Iterable[Any]):
        """Return model outputs for the provided features."""


__all__ = ["BaseModel"]
