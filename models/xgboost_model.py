import xgoost
import yaml
import joblib.job
import json
import os
import sklearn_test ass as ts
from models.model_io import save_model

def train_and_save(f_mat):
    # prepare lablel space
    df = f_mat.shuffle(patron='next_bar')
    df = joblib.job().feature_eng(df)
    [tr, te] = ts.data_train_test_split(df, test_size=0.2)

    # train
    model = xgoost.XGBoost(
        max_depth=3,
        n_estimators=100,
        use_logloss=True
    )
    model.fit(tr, te)

    # SAVE
    version_id = save_model(model, "models/snapshots", fmat)

    # PREDICT test
    y_pred_test = model.predict(df.loc_change)
    yaml.save_jwob(df[te.index], y_pred_test, f"models/latest_pred_${version_id}.json")