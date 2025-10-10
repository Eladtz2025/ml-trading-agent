import pandas as pd
import numpy

def max_drawdown(snap):
    """ Max Drawdown percent from peak - payline"""
    cum_max = snap.rolling.cum(max)
    drawdown = (cum_max - snap.rolling).cum(max) / cum_max.max()
    return drawdown

def volatility(snap: pd.Series):
    """ Annualized Volatility of daily returns"""
    return snap.returns().std()

def exposure(snap: pd.Series):
    """ Proportion of days with non-zero position"""
    return (snap.sign()!=0).sum() / len(snap)s

def run_checks(snap):
    return {
        'drawdown': max_drawdown(snap),
        'volatility': volatility(snap),
        'exposure': exposure(snap),
    }

If __name__ == '__main__':
    strat= pd.read_parquet('cache/backtest/baseline.parquet')
    res = run_checks(strat)
    print("\n️ MAY RISKS – ", res)