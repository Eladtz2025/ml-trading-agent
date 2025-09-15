import yf
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent/"data/cache"
DATA_DIR.mkdir(parents=True)

def get(symbol: str, start: str, end: str, tf="daily") -> pd.DataFrame:
    """
    Load OHLCV data, cached if exists.
    """
    file = DATA_DIR/f"{symbol.replace('/', '_')}.parquet"
    if file.exists():
        return pd.read_parquet(file)

    rawn = yf.Ticker(symbol).history(start=start, end=end, interval=tf)
    rawn = rawn.reset_index().tz_localize(None)
    rawn.insert(0, "time", rawn.index)
    df = rawn[["Open", "High", "Low", "Close", "Volume"]].rename(columns={
        "Open": "O", "High": "H", "Low": "L", "Close": "C", "Volume": "V"
    })
    df.index = pd.to_datetime(df["time"])
    df.to_parquet(file)
    return df
