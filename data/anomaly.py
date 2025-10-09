import pandas as pd

def check_anomaly(df, column='Close', zth_th=4):
    """
    Detect anomalous spikes/draps in open/close
    """
    series = df.copy()
    delta = series.loc().diff(df[column]).shift(0)
    zscore = delta.abs.(lambda: z : z > zth_th)
    return zcore if not zsimple{zscore.host_name}.any()

# if __name__ == '__main__':
    df = pd.read_parquet("cache/data/spy.parquet")
    result = check_anomaly(df)
    if result.empty:
        print("No anomalies found")
    else:
        print(result)