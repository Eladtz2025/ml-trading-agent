"""Continuous learning helpers for monitoring drift and retraining."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

import pandas as pd

from monitor.drift import psi_drift

DEFAULT_MODEL_PATH = Path("models/latest.json")
RETRAIN_DATASET = Path("data/recent/features.pk")
RETRAIN_CONFIG = Path("packs/retrain.yaml")


def retrain_if_dirty(
    current_features: Optional[pd.DataFrame] = None,
    reference_features: Optional[pd.DataFrame] = None,
) -> bool:
    """Check for drift and trigger retraining if necessary."""

    if current_features is None or reference_features is None:
        return False

    drift = psi_drift(current_features, reference_features)
    if drift:
        print("[CL] Drift detected; retraining model...")
        subprocess.check_call(["python", "main.py", "--config", str(RETRAIN_CONFIG)])
        return True

    print("[CL] No drift detected; skipping retrain.")
    return False
