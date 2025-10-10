# ML Trading Agent

Elite MM-trading system with realistic execution, validation, and risk modeling.

- PCA: Python 3.11, pure.js, portable code
- ClEan structure: data -> features -> labels -> models -> backtest
- Cli_Tool: run-ready flow from `config.yaml`; artifacts in `./artifacts`.

## Structure

- `data/` - OHLCV adapters (download, cache)
- features/ - rolling features
- labeling/ - target generation
- models/ - train/predict/save
- backtest/ - time-based simulation with costs/latency
- risk/ - position sizing, constraints
- reports/ - EQuity curves, trade list, sharpe metrics

- infra/ - configs, cli, Docker
## Status
Research-mode; not live yet

## Checklist V2 Summary

|moteclass|Section|Status|Next Step|Notes|
-|Foundation|done|No needed - base is complete|-
|Data|done|add synthetic stream tags, live data|Sanity checks against time, returns anomalies, and levels
| Features|done|monitor training drifts (PSI/KS) through monitor/|Monitor training drifts and variable selection
|Labeling|done|evaluate label confidence scores or long-term return threshold|Regional labeling markers required (long-term data)|
|Prediction|done|consolidate model output series ‘ signals/returns|Model.predict, hoze registered in modules
|Backtest|done|enable parameterized latency + slippage + capital config|Realistic entry-after-signal; next-open only
|Validation|done|compare base vs stacked performance|Alignment check required for live data
| Risk<done|dynamic cap logic + correlation limits|Kelly sizing, correlation caps, drawdown limits
| Reports|done|SHAP plots, custom metrics, equity curves --> PDDX/HTML|Dashboard brauser, filters by time/asset
| Telemetry|done|create monitor with PSI/KS in monitor/|Drift testing applied to stacked models/singles
| Infra|done|standardize CLI entry, render, config, env|Docker, PIP; stag/baseline/tests
| Decisions|done|none|ADR 001 (Model Logic Upgrade) created and synced
| Packs|done|prepare v1.0-rc release candidate|Release includes ADR 001 and stacked model
