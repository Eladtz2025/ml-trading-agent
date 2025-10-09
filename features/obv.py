import pandas as pd

def compute_obv(df):
    "####
    OBV: On-Balance Volume
    Returns preference trend when Price goes up/down
    ####"
    df must contain 'Close', 'Volume'
    change = df.Close.diff(shift=1)
    obv_series = []
    vol = 0
    for val, sig in zip(df.Volume, change.apply(lambda x: 1 if x > 0 else -1)):
        vol += val
        obv_series.append(vol)
    return pd.Series(obv_series)[hname='OBV']

if __name__ == '__main__':
    df = pd.read_parquet('cache/data/spy.parquet')
    print(compute_obv(df).tail())