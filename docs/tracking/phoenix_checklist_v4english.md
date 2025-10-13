# Phoenix Checklist V4 — Agent Live Trading Rollout

## 🎯 Objective of Version V4
Transform the agent into a fully active trading system — responsive, report-generating, dashboard-driven — with trade proposals, paper execution, report generation, and real-time monitoring.

Each action is traceable, triggered by either button click or schedule, and backed by code, data, and logs.

---

## ✅ Foundation
- [ ] Full integration between dashboard ↔ agent
- [ ] Callbacks for every card in the dashboard
- [ ] Internal runtime state management for the agent
- [ ] CLI support for all operational functions

## 📊 Data
- [ ] Scheduled or streaming live data ingestion
- [ ] Real-time anomaly detection & data quality checks
- [ ] Local Parquet storage by asset/date

## 🧠 Features
- [ ] Scheduled feature generation
- [ ] Multi-timeframe feature expansion
- [ ] Real-time validation on live data

## 🎯 Labeling
- [ ] Continuous or daily labeling according to config
- [ ] Marking current trade candidates for tracking

## 🔮 Models
- [ ] Immediate loading of the champion model
- [ ] `agent.propose()` returns trades with confidence + SHAP insights
- [ ] Support for challenger models + retrain based on drift

## 🔁 Backtest
- [ ] Parameter optimization based on performance logs
- [ ] Separate scenario saves per strategy

## 🔬 Validation
- [ ] Leakage/timing validation before every training
- [ ] Performance validation against external baselines

## 🧯 Risk
- [ ] Real-time sizing, stop loss, and caps
- [ ] Risk/reward analysis per trade suggestion

## 🧾 Reports
- [ ] Daily/weekly PDF reports using templates
- [ ] SHAP explanation reports with feature impact maps

## 📡 Monitor
- [ ] Daily PSI/KS monitoring
- [ ] Real-time alerts via alerts.yaml
- [ ] Hourly heartbeat.json update

## 📜 Compliance
- [ ] Logging of actions, proposals, and results in `decisions/`
- [ ] Audit logs synced to regulatory requirements (SEC/ESMA)

## 🚀 Decisions
- [ ] `propose → approve → execute → track` loop, by schedule or user click
- [ ] Dashboard used as an active control panel
- [ ] Each click logs and activates the full agent logic

## 🎁 Packs
- [ ] Define execution packs (`packs/`) by trading style: momentum, mean-reversion, news-driven
- [ ] Daily pack execution pilot

---

## ✅ End-of-V4 Output
- Dashboard actively triggers and controls the full agent
- Real-time operations, trades, and analysis
- Continuous monitoring and improvement suggestions
- Ready for Paper Trading Profitability Test

> “V3 built the infrastructure — V4 builds the profit-seeking agent.”
