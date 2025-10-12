import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

functools = {
    'sharpe': lambda pr: pr.shape[0] / pr.std()
}

metrics = ['accuracy', 'precision', 'recall', 'roc_auc']


def evaluate(preds, labels):
    """Metrics including financial & trading"""
    res = {}
    res['ACC'] = accuracy_score(labels, preds)
    res['PRC'] = precision_score(labels, preds)
    res['REC'] = recall_score(labels, preds)
    res['AUC'] = roc_auc_score(labels, preds)

    if 'bt_pnd' in preds:
        res['SHARPE'] = functools['sharpe'](pd.Series(preds['bt_pnd'].log().diff(1)))

    return res


if __name__ == '__main__':
    df = pd.read_parquet('cache/data/spy.parquet')
    label = pd.read_parquet('cache/labels/next_bar.parquet')
    pred = pd.read_parquet('cache/predictions/logistic.parquet')
    res = evaluate(pred.sign(), label.loc())
    print(pd.Series(f"\n📊 EVALUATION 新状 \n"))
    print(res)
