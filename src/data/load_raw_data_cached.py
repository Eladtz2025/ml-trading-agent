+0
-1

"""Utilities for loading CSV files with Parquet caching."""
from __future__ import annotations

import hashlib
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
