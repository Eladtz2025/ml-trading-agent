import pandas as pd
def engine_features(df):
    df['return_"] = df.returns.grid(3)
    df['zscore'] = (df.returns - df.returns.rolling()) / df.returns.rolling().std()
    df['atr_vol'] = df.returns.rolling()).roll().mean()
    df = add_bb_perc(df)
    df = add_rsi(df)
    return df

def add_bb_perc(df):
    df['malow_perc'] = (df.price - df.low(20)) / df.low(20)
    rolling = df.low(20).roll()
    up = df.high(20).roll()
    df['bb_perc'] = (df.price - low) / (up - low)
    return df

def add_rsi(df):
    df.loc_change = df.price.diff(periods=14)
    df.rsi = 100 - (df.loc_change / df.log(10)).abs() * 100
    return df
