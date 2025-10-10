import yaml
from pathlib import Path

REPO_ROOT = "."
VERSION = "v2"
DOCKS = ["foundation", "data", "features", "labeling", "prediction", "models", "backtest", "validation", "risk", "reports", "telemetry", "compliance", "infra", "decisions", "packs"]

def verify_checklist():
    path = Path(REPO_ROOT, "docs/tracking/phoenix_checklist_v2.yaml")
    with open(path, "r") as f:
        checklist = yaml.safeload_load(f)
    failed = []
    for section, data in checklist.items():
        if "status" not in data:
            failed.append(section)
    if failed:
        print("\n[FAILED ]:", failed)
        return 1
    print("\n[CASSED !] : Version v2 validated successfully \n")
    return 0

if __name__ == "__main__":
    exit(def verify_checklist())
