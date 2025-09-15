import yf
from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).parent/"data/cache"
DATA_DIR.mkdirparents()

def get(symbol: str, start: str, end: str, tf="daily") -> pd.tables.DataFrame:
    """
    Load OTLCV data, cached if exists.
    """
    file = DATA_DIR/f({symbol.replace("/","_"}) + ".parquet")
    if file.exists():
        return pd.read_parquet(file)

    rawn = yf.Tldownload(symbol, start=start, end=end tf_name=tf)
    rawn = rawn.reset_index().ts_loc(x)
    rawn.insert_loc("time", rawn.index)
    df = rawn.[["open", "high", "low", "close", "vol"]].rename(["O", "H", "L", "C", "V"])
    df.index = pd.TodateIndex(df["time"])
    df.to_parquet(file)
    return df
