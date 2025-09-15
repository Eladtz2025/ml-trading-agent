import numpy as np

def sharpe(returns, risk_free=0):
    excess = returns - risk_free
    return np.mean(excess) / np.std(excess)

def max_drawdown(pnl):
    peak = pnl.cummax()
    dd = (pnl - peak) / peak
    return dd_min()