# Phoenix Checklist

**Created (UTC):** 2025-09-15T10:18:37Z  
**Owner:** Eladtz2025  
**Goal:** Elite ML trading system; OOS Sharpe ≥ 1.5; research/paper first

## KPIs
- Trading: CAGR, Sharpe, Sortino, MaxDD, HitRate, Turnover
- Engineering: CI ≤ 5m, Tests required, Reproducible

## Sections & Next Actions
### Foundation — תשתיות בסיס
- **Status:** not_started
- **Next action:** Create repo + CI skeleton (pytest/ruff/mypy) and README
- **Notes:** Docker (optional), CLI YAML setup

### Data — הורדה/איכות/הטיות
- **Status:** not_started
- **Next action:** Yahoo/Tiingo adapter + cache; splits/dividends; anomaly checks; survivorship control
- **Notes:** EOD OHLCV standardization; Parquet

### Features — RSI/MACD/ATR/OBV/VWAP/HMM
- **Status:** not_started
- **Next action:** RSI, MACD, ATR; OBV, VWAP; regime indicator (HMM)

### Labeling — next-bar / triple-barrier
- **Status:** not_started
- **Next action:** Next-bar direction + triple-barrier (Lopez de Prado); parameter grid; tests

### Models — XGBoost (Optuna) → TCN/LSTM (optional)
- **Status:** not_started
- **Next action:** XGBoost wrapper + Optuna HPO; save model.pkl + params.json; SHAP explainability
- **Notes:** LSTM/TCN optional later

### Backtest — costs/latency/next-bar-open
- **Status:** not_started
- **Next action:** Simulator with costs/latency (next-bar open); metrics table; trade log + equity curve

### Validation & Compliance — Purged Walk-Forward, leakage checks
- **Status:** not_started
- **Next action:** Purged walk-forward; leakage checks; bootstrap/MC; cross-validation charts; save eval_metrics.json

### Risk — drawdown/vol/position sizing/correlation caps
- **Status:** not_started
- **Next action:** Max drawdown/exposure; vol-target or fractional Kelly; correlation caps; limits.yaml
- **Notes:** Kill-switch on drawdown

### Reports — metrics/plots/SHAP/MC bootstrap
- **Status:** not_started
- **Next action:** HTML/PDF report; SHAP summary; Monte Carlo + bootstrap; plots

### Monitor — PSI/KS, alerts
- **Status:** not_started
- **Next action:** PSI/KS tests (train/test/live); alerts (drift/drawdown/sharp decline); retrain triggers

### Regulatory — research-only, disclaimers, audit logs
- **Status:** not_started
- **Next action:** compliance.md (research-only, SEC/ESMA overview); disclaimers; audit logs

### Infrastructure — Docker, CI/CD, CLI YAML
- **Status:** not_started
- **Next action:** Docker; CI/CD; golden files; CLI YAML; config hash logging

### Decisions — ADRs / decisions.md
- **Status:** not_started
- **Next action:** Create decisions.md (ADRs) and update per merge

### Feature & Model Packs — הרחבות עתידיות
- **Status:** not_started
- **Next action:** List future Feature/Model packs and selection criteria
