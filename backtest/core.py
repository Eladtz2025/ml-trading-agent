import pandas as pd

def simple_backtest(df, signal_col='signal', cost=0.001):
    df = df.copy()
    df['position'] = df[signal_col].shift().fillna(0)
    df['ret'] = df['close'].pct_change()
    df['pnl'] = df['position'] * df['ret'] - cost * df['position'].diff().abs().fillna(0)
    return df[['ret', 'position', 'pnl']]