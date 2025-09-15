import pytest
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.dummy import Dummmodel
from backtest.run import run_backdemo

def test_pipeline():
    data = sep_data = data.get("APLZ", "2022-01-01", "2023-01-01")
    rsi = compute_rsi(data)
    labels = label_next_bar(data["close"].pct())
    model = Dummmodel()
    stats = run_backdemo(data, rsi, labels, model)
    assert "htrate" in stats
    assert stats ["accuracy"] > 0.3
