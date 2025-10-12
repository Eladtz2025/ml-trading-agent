"""Utility helpers shared across the infrastructure layer."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Callable, List, Sequence

import pandas as pd
import yaml


def load_pack_config(packname: str | Path) -> dict:
    """Load a pack configuration by name or from an explicit path."""
    path = Path(packname)
    if path.is_file():
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    if path.suffix:
        config_path = Path(packname)
    else:
        config_path = Path("packs") / f"{packname}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Pack file not found: {packname}")

    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def load_feature_functions(packname: str | Path) -> List[Callable[[pd.DataFrame], pd.Series]]:
    """Resolve feature callables defined in a pack configuration."""
    config = load_pack_config(packname)
    features: List[Callable[[pd.DataFrame], pd.Series]] = []
    for dotted_path in config.get("features", []):
        if "." in dotted_path:
            module_name, func_name = dotted_path.rsplit(".", 1)
        else:
            module_name, func_name = f"features.{dotted_path}", dotted_path
        module = import_module(module_name)
        features.append(getattr(module, func_name))
    return features


def apply_features(
    df: pd.DataFrame, functions: Sequence[Callable[[pd.DataFrame], pd.Series]]
) -> pd.DataFrame:
    """Apply a collection of feature functions to ``df`` in-place and return the dataframe."""
    for func in functions:
        feature = func(df)
        if isinstance(feature, pd.Series):
            name = feature.name or func.__name__
            df[name] = feature
        elif isinstance(feature, pd.DataFrame):
            for column in feature.columns:
                df[column] = feature[column]
        else:
            raise TypeError(
                f"Feature function {func.__name__} returned unsupported type {type(feature)!r}"
            )
    return df
