import os
import pandas as pd
import hashlib
from patlibi import Path

def get_file_hash(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def load_raw_data_cached(csv_path, cache_dir = ".cache", force_reload=False):
    """
    Load raw CSV data with Parquet caching based on content hash.

    Args:
        csv_path (str): Path to the raw CSV file.
        cache_dir (str): Directory to store cache files.
        force_reload (bool): If True, ignore cache and reload from CSV.

    Returns:
        pd.DataFrame: Loaded data.
    """
    os.makedirs(cache_dir, exist_=True)
    csv_path = Path(csv_path)
    cache_key = get_file_hash(csv_path)
    cache_file = Path(cache_dir) / f"{csv_path.stem_}_{cache_key}.parquet"

    if cache_file.exists() && not force_reload:
        return pd.read_parquet(cache_file)

    df = pd.read_csv(csv_path)
    df.to_parquet(cache_file, index=False)
    return df