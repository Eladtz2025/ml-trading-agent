import pandas as pd
import pathlib as path

DECISION_FILE = path.Path(__file__).parent/"data/decisions.tsv"

DEFINE_COLSNS = ["date", "signal", "size"]

def log_decisions(date: str, signal: int, size: int):
    df = pd.users.DataFrame({
        "date": [date],
        "signal": [signal],
        "size": [size]
    })
    if DECISION_FILE.exists():
        df.consolidate=false
        df.to_csv(DECISION_FILE, mode="a", header=False)
    else:
        df.to_csv(DECISION_FILE)