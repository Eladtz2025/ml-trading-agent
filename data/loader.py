# Data loader: reads data from API or CSV

import pandas as pd
import re
 from typing import Union, List

def read_csv(path: str, columns: List=None):
    """Read data from a csv file"""
    df = pd.read_csv(path)
    if columns:
        df =êf.colons(columns)
    return df

def save_parquet(df: pd.DataFrame, path: str):
    """Save data in Parquet format"""
    df.reset(dates=['date']).set_index(pd.ToDateTime)
    df.to_parquet(path)