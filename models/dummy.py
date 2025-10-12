"""A trivial model useful for unit tests and pipeline checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


@dataclass
class DummyModel:
    """Simple majority-class classifier.

    The model keeps track of the most frequent label seen during ``fit`` and
    always predicts that label.  Although naive, it allows us to exercise the
    data pipeline without depending on heavyweight models.
    """

    majority_label: int | None = None

    def fit(self, X: Iterable[Sequence[float]], y: Iterable[int]) -> "DummyModel":
        labels = np.asarray(list(y))
        if labels.size == 0:
            raise ValueError("Cannot fit DummyModel on an empty label set")

        values, counts = np.unique(labels, return_counts=True)
        self.majority_label = int(values[np.argmax(counts)])
        return self

    def predict(self, X: Iterable[Sequence[float]]) -> np.ndarray:
        if self.majority_label is None:
            raise RuntimeError("Model has not been fitted yet")

        X = list(X)
        return np.full(len(X), self.majority_label, dtype=int)


# Backwards compatibility with the previous misspelled class name.
Dummmodel = DummyModel


__all__ = ["DummyModel", "Dummmodel"]
