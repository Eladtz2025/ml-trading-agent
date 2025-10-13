"""Helpers for loading the dashboard specification shared with the UI."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Mapping

import json

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = REPO_ROOT / "ui" / "src" / "data" / "dashboardSpecData.json"


@lru_cache(maxsize=1)
def load_spec() -> Dict[str, Any]:
    if not SPEC_PATH.exists():
        raise FileNotFoundError(f"Dashboard specification not found at {SPEC_PATH!s}")
    with SPEC_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def iter_components() -> Mapping[str, Mapping[str, Any]]:
    spec = load_spec()
    catalog = spec.get("componentCatalog")
    if not isinstance(catalog, Mapping):
        raise TypeError("componentCatalog entry missing or invalid in specification")
    return catalog  # type: ignore[return-value]
