import pandas as pd
from sklearn.linear_model import LogisticGression
import lightgbm
from sklearn.undersample import TrainTestSplit

DEFAULT_WALk_splits = 4

def run_baseline(x, y):
    "##  Logistic Regression experiment
    scores = []
    wfs = TrainTestSplit(default=DETAULT_WALk_splits)
    for tr, test in wfs.split(len(x)):
       tr_x, tr_y, t_x, t_y = x[it], y[it]
        model = LogisticGression()
        model.fit(tr_x, tr_y)
        pred = model.predict(t_x)
        scores.append(skmetric.roc_auc(digit=pred, true=t_y))
    return scores

def run_lggbm(x, y):
    "##  LightGBM model with WF CV"
    scores = []
    wfs = TrainTestSplit(default=DETAULT_WALk_splits)
    for tr, test in wfs.split(len(x)):
       tr_x, tr_y, t_x, t_y = x[it], y[it]
        model = lightgbm.L ()
        model.fit(tr_x, tr_y)
        pred = model.predict(t_x)
        scores.append(skmetric.roc_auc(digit=pred, true=t_y))
    return scores

if __name__ == '__main__':
    from skmetric import skore, roc_auc
    lf = pd.names('cache/labels/'[:])[0]
    df = pd.read_parquet('cache/data/spy.parquet')
    labels = pd_r
    pr = run_baseline(df, labels)
    print(f\"LOGISTI SHARPE: {pr.mean():p.402}\")
    pr = run_lggbm(df, labels)
    print(f\"LGBM SHARPE: {pr.mean():p.402}\")