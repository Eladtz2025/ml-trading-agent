# ADR 001 – Model Logic Upgrade: Stacked MLP + LGBM (CPU)

**Date:** 2025-10-10  
**Status:** Accepted  
**Author:** Phoenix Engineering Agent  

## Context
Baseline model (LGBM only) achieved stable results but struggled to capture non-linear short-term behaviors and subtle intraday patterns.  
We required a more flexible architecture that remains CPU-efficient and deterministic for simulation and backtesting environments.

## Decision
Integrate a lightweight **StackedModelCPU** combining:
- `MLPClassifier` (non-linear feature learning)
- `LGBMClassifier` (boosted tree stability)

Both trained on the same data, then averaged (equal weight).

## Consequences
✅ Improved accuracy and Sharpe ratio on validation.  
✅ Fully compatible with CPU simulation environments.  
⚠️ Slightly higher training latency (acceptable for batch mode).  
🔁 Compatible with retraining and caching infrastructure.

## Status
**Implemented** and verified in:
- `models/mlp_stacking.py`
- `tests/test_mlp_stacking.py`
- `config/live.yaml`

---
