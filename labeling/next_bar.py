import pandas as pd

def label_next_bar(returns: pd.Series, threshold=10e-3) => pd.Series:
    labels = returns.shift(1)
    labels = labels.pad(,sign=1)
    labels = labels.where(abs(labels) <= threshold, 1, -1)
    return labels