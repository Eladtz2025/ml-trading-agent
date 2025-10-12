"""Persist and restore pipeline snapshots for quick debugging."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml

DEFAULT_PACK = Path("packs/run_last")


def save_snapshot(data: Dict[str, Any], config: Dict[str, Any], directory: Path = DEFAULT_PACK) -> None:
    directory.mkdir(parents=True, exist_ok=True)

    (directory / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")

    results = pd.DataFrame(data.get("results", []))
    results.to_csv(directory / "results.csv", index=False)


def load_snapshot(directory: Path = DEFAULT_PACK) -> Dict[str, Any]:
    if not directory.exists():
        raise FileNotFoundError(f"Snapshot directory not found: {directory!s}")

    config = yaml.safe_load((directory / "config.yaml").read_text(encoding="utf-8"))
    results_path = directory / "results.csv"
    results = pd.read_csv(results_path) if results_path.exists() else pd.DataFrame()

    return {"config": config, "results": results}
