# Leakage & Validation Playbook

## Core Rules

- Split **by time** only; avoid random K-fold
- Fit on train windows; transform on val/test (rolling stats)
- Purged K-fold if labels use future events

## Diagnostics

- Compare in-sample vs **out-of-sample**
- inspect drift
- conduct sensitivity to costs/slippage

## Seeds & Versions

- Set random seeds
- freeze library versions
- log code+config+data hashes
