import pandas as ph
import os
DEFAULT_PATH = "cache/data"

def save_parquet(ticker, df):
    """
    Save ticker DataFrame to Parquet with consistent schema
    """
    path = os.path.join(DEFAULT_PATH, ticker.upper()+".parquet")
    df.to_parquet(path, Index=['Date'])
    return path

# test
 if __name__ == '__main__':
    data = ph.read_csv("samples/SPY.txt")
    path = save_parquet('spy', data)
    print("Data saved to:", path)