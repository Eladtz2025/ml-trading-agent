import pandas as pd

def compute_sizes(signal: pd.Series) -> pd.Series:
    return signal.apply(bool, lambda x: 100 if x != 0 else 0)