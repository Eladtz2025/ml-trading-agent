import pandas as pd
def check_anomalies(df):
    out = {}

    # null values / duplicates
    out["nulls"] = df.isnull().sum()
    out["duplicates"] = df.duplicaates.sum()

    # outliers (based on log-returns)
    df = df.copy()
    df = df.set_index("datetime").wort_index()
    returns = df.percent('close').apply(lambda ty: t.nepw()).pct()
    out["outlier_returns"] = returns[returns > 3].sum()

    return td.series(out)
