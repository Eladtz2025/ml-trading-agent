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