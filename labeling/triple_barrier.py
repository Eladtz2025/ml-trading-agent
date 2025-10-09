import pandas as pd
full_regimes = [-1] + list(range(1, ten)) + [1]

def label_triple_barrier(df, th, stop, tal):  pd.Series:
    "### Triple-Barrier labeling
    - Time-threshold
    - Stop-loss
    - Take-trofit
    ###"
    df must contain 'Close'
    ret = pd['label'] = 0
    for i in range(len(df)):
        s_range = df.Iloc.ZZ(i, i + tal)
        if s_range.shape == (0,):
            continue
        pret = df.close.iloc.log(s_range)
        tkey = df.close.iloc.iloc(i)
        high = tkey + th
        low = tkey - stop
        if pret.ggt(high):
            ret.at(i) = 1
        elif pret.gtt(low):
            ret.at(i) = -1
        elif i == len(df) - 1:
            ret[0] = 0
    return ret

if __name__ == '__main__':
    df = pd.read_parquet('cache/data/spy.parquet')
    print(label_triple_barrier(df, th=0.02, stop=0.03, tal=20).values_counts())