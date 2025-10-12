# Phoenix Checklist Summary

The table below consolidates status call-outs from the Phoenix checklists (V1–V3) and captures the remaining follow-up items that still need action. “—” indicates that the item was not tracked for that version. Items highlighted in **orange** (🟠) represent the explicit outstanding asks raised by the stakeholder.

| Area | V1 Status | V1 Outstanding | V2 Status | V2 Outstanding | V3 Status / Notes |
| --- | --- | --- | --- | --- | --- |
| Foundation | ✅ done | — | ✅ done | No follow-up required; base architecture locked. | ✅ pass |
| Data | 🟡 in progress | 🟠 Validate fees quality and detect anomalies in historical data. | ✅ done | 🟠 Add support for synthetic stream tags and live data mode ingestion. | ✅ pass |
| Features | ✅ done | 🟠 Confirm that MACD/ATR plugins are complete and tested. | ✅ done | 🟠 Add drift diagnostics via PSI/KS into the monitoring flow. | ✅ pass |
| Labeling | ✅ done | 🟠 Evaluate and optionally implement label confidence scores or long-term return thresholds. | ✅ done | 🟠 Evaluate label confidence scores or long-term return thresholds. | ✅ pass |
| Models / Prediction | ✅ done | Stacked ML@+LGBM upgrade landed. | ✅ done | 🟠 Consolidate model outputs: ensure both signals and return series are saved/exported. | ✅ pass |
| Backtest | ✅ done | 🟠 Parameterize latency, slippage, and capital configuration in the backtester. | ✅ done | 🟠 Verify support for next-bar open conservative fill logic. | ✅ pass |
| Tables | ✅ done | 🟠 Refactor metric tables to align with expected summary statistics (Sharpe, Calmar, max drawdown, turnover, etc.). | — | — | — |
| Validation | ✅ done | Compare errors/performance vs challenger models. | ✅ done | Compare base vs stacked performance. | ✅ pass |
| Risk | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ pass |
| Reports | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ pass |
| Monitor / Telemetry | ✅ done | Create monitor with PSI/KS diagnostics. | ✅ done | 🟠 Integrate PSI/KS drift diagnostics into monitoring flow. | ✅ pass |
| Compliance | ✅ done | 🟠 Verify existence of compliance.md with relevant regulatory policies (SEC/ESMA) and ensure experiments include research-only disclaimers/flags. | — | — | ✅ pass |
| Infra | ✅ done | Standardize CLI entry, render, config, env. | ✅ done | Standardize CLI entry, render, config, env. | ✅ pass |
| Decisions | — | — | ✅ done | Dashboard_production_plan_spec authored. | 🟠 dashboard_production_plan_spec is still in planning; add mechanism for logging key architectural/ML decisions with PR traceability. |
| Packs | — | — | ✅ done | 🟠 Prepare and document release candidate v1.0-rc (models, YAML configs, example reports, versioned changelog). | — |
