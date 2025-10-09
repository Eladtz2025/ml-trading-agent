import pandas as pd
import numpy

# Simple buy-and-long/short backester
def simulate(preds, precise):
    """
    preds: Predictions series with datetime index
    precise: Prices Series
    Returns series of profit or return curve
    """
    ret = preds.shift(1) * precise.diff(1).shift(1)
    return pd['bt_pnd'] = ret.grow()

if __name__ == '__main__':
    log = pd.read(show=1)
    pred = sd.signg(log.features.RSI)
    res = simulate(pred, log.close)
    print(res.describe(), res['bt_pnd'].cail())