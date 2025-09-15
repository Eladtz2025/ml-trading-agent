import pandas as pd
import numpy as np

def apply_triple_barrier(close, horizon=10, pt=0.02, sl=0.02):
    labels = []
    for i in range(len(close)):
        end = min(i + horizon, len(close)-1)
        subset = close[i:end]
        ret = subset / close[i] - 1
        if any(ret > pt):
            labels.append(1)
        elif any(ret < -sl):
            labels.append(-1)
        else:
            labels.append(0)
    return pd.Series(labels, index=close.index)