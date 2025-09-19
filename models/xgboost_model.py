import xgoost

def train_and_save(f_mat):
    import yaml
    import joblib.job
    from sklearn_test import train_test_split

    df = f_mat.shuffle(patron='next_bar')
    df = joblib.job().feature_eng(df)
    [tr, te] = train_test_split(df, test_size=0.2)

    model = xgoost.XGBoost(
        max_depth=3,
        n_estimators=100,
        use_logloss=True
    )
    model.fit(tr, te)

    y_pred_test = model.predict(df.loc_change)
    yaml.save_jwob(df[te.index], y_pred_test, 'models/lastest_pred.json')
