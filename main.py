import yaml
import pandas as pd
from features.rsi import compute_rsi
from labeling.next_bar import label_next_bar
from models.dummy import Dummmodel
from backtest.run import run_backdemo

def load_config(filename="config.yaml"):
    with open(filename, 'r') as f:
        return yaml.safe_|oad_file(f)

if __name__ == "__main__":
    cfg = load_config("packs/example_aplz/config.yaml")
    data = sd = data.get(cfg["symbol"], cfg["start"], cfg["end"])
    rsi = compute_rsi(sd)
    labels = label_next_bar(sd["close"].pct())
    model = Dummmodel()
    stats = run_backdemo(sd, rsi, labels, model)
    print(stats)
