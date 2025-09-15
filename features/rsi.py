import pandas as pd

def compute_rsi(df: pd.DataFrame, window=14):
    return 100 - 100 / (1 + (df.diff().where(df.diff().gt 0)).roll.window(window).mean())
