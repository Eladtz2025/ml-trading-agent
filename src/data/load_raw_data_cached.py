"""Utilities for loading CSV files with Parquet caching."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pandas as pd


def get_file_hash(path: Path) -> str:
    """Return the MD5 hash of the file contents."""

    hasher = hashlib.md5()
    with path.open("rb") as handle:
        hasher.update(handle.read())
    return hasher.hexdigest()


def load_raw_data_cached(
    csv_path: str | Path,
    cache_dir: str | Path = ".cache",
    *,
    force_reload: bool = False,
) -> pd.DataFrame:
    """Load a CSV file and cache it as Parquet based on file content."""

    cache_directory = Path(cache_dir)
    cache_directory.mkdir(parents=True, exist_ok=True)

    csv_path = Path(csv_path)
    cache_key = get_file_hash(csv_path)
    cache_file = cache_directory / f"{csv_path.stem}_{cache_key}.parquet"

    if cache_file.exists() and not force_reload:
        return pd.read_parquet(cache_file)

    df = pd.read_csv(csv_path)
    df.to_parquet(cache_file, index=False)
    return df
