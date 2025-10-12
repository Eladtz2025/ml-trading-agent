"""Utility to verify the engineering checklist document."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(".")
CHECKLIST_PATH = REPO_ROOT / "docs/tracking/phoenix_checklist_v2.yaml"


def verify_checklist() -> int:
    if not CHECKLIST_PATH.exists():
        print("Checklist file not found.")
        return 1

    with CHECKLIST_PATH.open("r", encoding="utf-8") as handle:
        checklist = yaml.safe_load(handle)

    failed = [section for section, data in checklist.items() if not data.get("status")]

    if failed:
        print("\n[FAILED]:", failed)
        return 1

    print("\n[PASSED]: Version v2 validated successfully\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(verify_checklist())
