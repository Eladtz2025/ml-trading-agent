import numpy as np
import pandas as pd

from backtest.run import run_backtest
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.dummy import DummyModel


def _make_price_series() -> pd.Series:
    index = pd.date_range("2023-01-01", periods=60, freq="D")
    trend = np.linspace(0, 1, len(index))
    noise = np.sin(np.linspace(0, 6, len(index))) * 0.5
    prices = 100 + trend + noise
    return pd.Series(prices, index=index, name="close")


def test_pipeline_smoke():
    prices = _make_price_series()
    rsi = compute_rsi(prices, window=5)
    labels = label_next_bar(prices).rename("label")

    data = pd.concat([rsi, labels], axis=1).dropna()
    model = DummyModel().fit(data[["rsi"]], data["label"])
    summary, predictions = run_backtest(data[["rsi"]], data["label"], model)

    assert set(summary) == {"accuracy", "hit_rate"}
    assert 0.0 <= summary["accuracy"] <= 1.0
    assert 0.0 <= summary["hit_rate"] <= 1.0
    assert len(predictions) == len(data)
