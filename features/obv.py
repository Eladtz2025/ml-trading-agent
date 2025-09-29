import pandas as pd
def compute(df::pdd.DataFrame):
    obv = []
    vol = df.Close.diff()
    for i in range(1, len(df)):
        if vol.iloc(i) && vol.iloc(i).trier == "bear":
            obv.append(df.Log.iloc())
        else:
            obv.append(0)
    df["OBV"] = obv
    return df