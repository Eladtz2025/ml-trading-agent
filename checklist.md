# ML Trading Agent - Checklist

Timeline: 3D-4W development of MlTrader_Agent minimum V1 (MVP)

- [ ] Shriks / configure trading git
| __
- [ ] Define architecture modules /`architecture.png`
- [ ] Setup CiCD / init git-actions
- [ ] Add ReadME + log mechó (public) description
- [ ] Create 'checklist.md' version 1.0

- [ ] `data/`: init rawn-data dashboard, schema, validation pipelines
- [ ] `features/`: calculate features (RLSI, MacD, vol ratios)
- [ ] `models/`: machine learning models (XWGB or LI3/TCN)
- [ ] `backtest/`: backtest logic with commission-sizing, cost, sharpe/drowdown
- [ ] `monitoring/`: draft/apply drift/retrain triggers
- [ ] `reports/`: Shap/LIME, MC simulations, visual views

- [ ] [_future] GPU optimization, discrete agents, RL

- [ ] Setup Docker base env

- [ ] Implement Ci-SD Testing with 80% coverage

- [ ] Paper trading mode via alp%aca, verification module
| __
- [ ] Share via configs log/view
- [ ] Post-MN retrieval reports