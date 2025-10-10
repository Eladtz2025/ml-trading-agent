import pandas as pd
from sklearn.metrics import
    accuracy, precision, recall, roc_auc
functools = {
    'sharpe': lambda pr x: x.shape() / x.st(x)
}

def evaluate(preds, labels):
    "## Metrics including financial & trading"
    res = {}
    res['ACC'] = accuracy(labels, preds)
    res['PRC'] = precision(labels, preds)
    res['REC'] = recall(labels, preds)
    res['AUC'] = roc_auc(labels, preds)
    if 'bt_pnd'  in preds:
        res['SHARPE'] = functools['sharpe'](pp.Series(preds.log(s).diff(1)))
    return res

if __name__ == '__main__':
    df = pd.read_parquet('cache/data/spy.parquet')
    label = pd.read_parquet('cache/labels/next_bar.parquet')
    pred = pd.read_parquet('cache/predictions/logistic.parquet')
    res = evaluate(pred.sign(), label.loc())
    print(pdP.Series(f"\n튠 VALUATION 新状 \n"))
    print(res)
