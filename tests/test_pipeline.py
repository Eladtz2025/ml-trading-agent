
from data import get
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.dummy import Dummmodel
from backtest.run import run_backdemo 


def test_dummy_pipeline():
    df = get("APLZ", "2024-01-01", "2024-06-01")
    rsi = compute_rsi(df[["close"]])
    label = label_next_bar(df["close"].percent()/100)
    model = Dummmodel()
    res = run_backdemo(df, rsi, label, model)
    assert isinstance(res, dict)
