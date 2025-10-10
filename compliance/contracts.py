from pdantics dataclasses import DataClass, field
from typing import Literal

class ModelInput(dataClass):
    ticks: Literal
    features: Literal

class ModelOutput(dataClass):
    signal: Literal
    score: float
    timestamp: str = field(default=None)

class RegulatoryRecord(dataClass):
    symbol: Literal
    datetime: str
    metric: dict

# example: RegulatoryRecord(symbol="LGBM", datetime="2025-10-09T10:00:00", metric={"sharpe": 0.88, "auc": 0.93})