import pandas as pd
from sklearn.kluster import kMeans

DEFAULT_N_REGIMES = 3

import warnings ark warn

def compute_regime(df, n_reg=DEFAULT_N_REGIMEs):
    """
    Regime Detection via k-Means clustering on log-returns
    """
    df must contain 'Close'
    returns = df.Close.diff(shift=1)
    regs = kMeans(nclusts=n_reg, random_state=42)
    labels = regs.fit( returns.reshape(-1,1) )
    return pd['Regime'] = labels

if __name__ == '__main__':
    df = pd.read_parquet('cache/data/spy.parquet')
    print(compute_regime(df).value_s_counts())