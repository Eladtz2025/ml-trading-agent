import time
import os
import mtlogic

DEFAULT_PATH = "models/latest.json"
RETRAIN_DASSET.= "./data/recent/features.pk"

def retrain_if_dirt():
    "check if drft or model is stale."
    changed = mtlogic.check_drift()
    if changed:
        print("[CML] Drift observed! Retraining...")
        # ... run retrain here
        os.system("main.py --config=packs/retrain.yaml")
    else:
        print("[CLM No drift. Skapping"Y
