# Phoenix Release Candidate v1.0-rc

This pack bundles the artefacts required to promote Phoenix into the production candidate stage. It includes the consolidated model outputs, configuration files, and example reports showcasing monitoring enhancements.

## Contents
- `models/` – Serialized estimator (`model_latest.joblib`) and associated metadata files.
- `config/` – YAML configuration for live ingestion, backtest defaults, and monitoring thresholds.
- `reports/` – Example summary reports with research-only disclaimers.
- `CHANGELOG.md` – Version history describing key changes in this release.

## Promotion Checklist
1. Validate fee quality report and anomaly scans (see `data/fees_quality.py`).
2. Run monitoring flow to produce PSI/KS metrics and attach output to compliance review.
3. Export decision log entry referencing PR and attach to compliance package.
4. Obtain sign-off from Compliance, Risk, and Engineering leads before deploying.
