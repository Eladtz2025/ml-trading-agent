# Dashboard Production Plan Spec

## Objective
Deliver a production-ready Phoenix monitoring dashboard that surfaces live trading metrics, risk controls, and compliance attestations.

## Milestones
1. **MVP Instrumentation (Week 1)**
   - Wire existing monitoring PSI/KS outputs into the dashboard data layer.
   - Surface latency, slippage, and capital utilisation metrics from the backtest engine.
2. **Risk & Compliance (Week 2)**
   - Embed research-mode disclaimer toggles and compliance checklist status widgets.
   - Add drill-down views for model metadata (config, git hash, version) exported from the consolidated model outputs.
3. **Production Hardening (Week 3)**
   - Implement auth (SSO) and role-based access for compliance reviewers.
   - Enable release pack promotion workflow (see `packs/releases/v1.0-rc`).

## Success Criteria
- Dashboard refresh latency < 5 minutes with live data ingestion.
- All widgets link back to a decision log entry ensuring traceability to the responsible PR.
- Exported PDF reports include the research-only disclaimer automatically.

## Owners
- Product: Phoenix Ops
- Engineering: Quant Platform Team
- Compliance: Regulatory Partnerships
