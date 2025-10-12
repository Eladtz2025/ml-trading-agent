"""Utilities for loading CSV files with Parquet caching."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Final

import pandas as pd


DEFAULT_CACHE_DIR: Final[str] = ".cache"


def get_file_hash(path: Path) -> str:
    """Return the MD5 hash of the file contents."""

    hasher = hashlib.md5()
    with path.open("rb") as handle:
        hasher.update(handle.read())
    return hasher.hexdigest()


def _build_cache_path(csv_path: Path, cache_dir: Path, file_hash: str) -> Path:
    """Create the cache file path based on the CSV file name and hash."""

    stem = csv_path.stem
    return cache_dir / f"{stem}-{file_hash}.parquet"


def load_raw_data_cached(
    csv_path: str | Path,
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
    *,
    force_reload: bool = False,
) -> pd.DataFrame:
    """Load a CSV file and cache it as Parquet based on file content.

    Args:
        csv_path: Location of the CSV file to load.
        cache_dir: Directory where cache files should be stored.
        force_reload: Whether to bypass the cache and reload the CSV file.

    Returns:
        A ``pandas.DataFrame`` containing the data from the CSV file.
    """

    csv_file = Path(csv_path).expanduser().resolve()
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    cache_directory = Path(cache_dir).expanduser()
    cache_directory.mkdir(parents=True, exist_ok=True)

    cache_path = _build_cache_path(csv_file, cache_directory, get_file_hash(csv_file))

    if not force_reload and cache_path.exists():
        return pd.read_parquet(cache_path)

    dataframe = pd.read_csv(csv_file)
    dataframe.to_parquet(cache_path)
    return dataframe
