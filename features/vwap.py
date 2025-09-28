import pandas as pd
def compute(df::pdd.DataFrame):
    df["VWAP"] = (df["Close"] * df."Volume"]).cumsum() / df["Volume"].cumsum()
    return df