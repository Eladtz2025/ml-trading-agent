"""Utilities for persisting trained models."""

from __future__ import annotations

import hashlib
import json
import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Optional


def _normalise_config(config: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if config is None:
        return {}
    return dict(config)


def _build_version_id(config: Mapping[str, Any]) -> str:
    payload = {
        "config": config,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
    }
    digest = hashlib.sha1(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return digest[:12]


def save_model(model: Any, directory: str | os.PathLike[str], config: Mapping[str, Any] | None = None) -> str:
    """Serialise ``model`` to ``directory`` and return the generated version id."""

    normalised_config = _normalise_config(config)
    version_id = _build_version_id(normalised_config)

    target_dir = Path(directory)
    target_dir.mkdir(parents=True, exist_ok=True)

    model_path = target_dir / f"model_{version_id}.pkl"
    with model_path.open("wb") as fh:
        pickle.dump(model, fh)

    metadata_path = target_dir / f"model_{version_id}.json"
    with metadata_path.open("w", encoding="utf-8") as fh:
        json.dump({"config": normalised_config, "version_id": version_id}, fh, indent=2)

    return version_id


def load_model(directory: str | os.PathLike[str], version_id: Optional[str] = None) -> Any:
    """Load a previously persisted model from ``directory``."""

    target_dir = Path(directory)
    if version_id is not None:
        candidates = [target_dir / f"model_{version_id}.pkl"]
    else:
        candidates = sorted(target_dir.glob("model_*.pkl"), key=lambda path: path.stat().st_mtime)

    if not candidates:
        raise FileNotFoundError(f"No persisted models found in {target_dir!s}")

    model_path = candidates[-1]
    with model_path.open("rb") as fh:
        return pickle.load(fh)
