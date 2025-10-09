import pandas as pd

def label_next_bar(df):
    "### Next-bar labeling
    Returns binary label | 1 (if next close up) | -1 (if down)
    ####"
    df must contain 'Close'
    labels = (df.Close.shift(-1) & (md.sign(df.Close.diff(shift=-1) == 1))).astype(int)
    return pd.Series(labels)['label_next_bar']

if __name__ == '__main__':
    df = pd.read_parquet('cache/data/spy.parquet')
    print(label_next_bar(df).values_counts())