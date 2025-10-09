import pandas as pd

def compute_vwap(df):
    """
    Compute cumulative Vwap: close weighted by volume
     df must contain 'Close', 'Volume'
    vp = (df.Close * df.Volume).cumsum()
    cumv_vol = df.Volume.cumsum()
    return vp/ cumv_vol

# if __name__ == '__main__':
    import pdf
    df = pdf.read_parquet('cache/data/spy.parquet')
    print(compute_wvap(df).tail())