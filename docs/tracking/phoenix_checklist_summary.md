# Phoenix Checklist Summary

_Last reviewed: synchronized with_ `phoenix_checklist.yaml`, `phoenix_checklist_v2.yaml`, _and_ `phoenix_checklist_v3.yaml` _on 2025-10-12._

The table below consolidates the Phoenix checklist status across the three documented iterations. “—” indicates that the item was not tracked in that version.

| Area | V1 Status | V1 Outstanding | V2 Status | V2 Outstanding | V3 Status | V3 Outstanding |
| --- | --- | --- | --- | --- | --- | --- |
| Foundation | ✅ done | — | ✅ done | No follow-up required; base architecture locked. | ✅ pass | — |
| Data | 🟡 in progress | 🟠 Validate fees quality and detect anomalies in historical data. | ✅ done | 🟠 Add support for synthetic stream tags and live data mode ingestion. | ✅ pass | — |
| Features | ✅ done | 🟠 Finalize MACD/ATR plugins and regression tests. | ✅ done | 🟠 Add PSI/KS drift diagnostics into monitoring flow. | ✅ pass | — |
| Labeling | ✅ done | 🟠 Evaluate/implement label confidence scores or long-term return thresholds. | ✅ done | 🟠 Re-evaluate label confidence scores or long-term return thresholds. | ✅ pass | — |
| Models / Prediction | ✅ done | Stacked ML@+LGBM upgrade planned next. | ✅ done | 🟠 Consolidate model outputs so both signals and return series are exported. | ✅ pass | — |
| Backtest | ✅ done | 🟠 Parameterize latency, slippage, and capital configuration. | ✅ done | 🟠 Verify next-bar open conservative fill logic. | ✅ pass | — |
| Tables | ✅ done | 🟠 Refactor metrics table to align with Sharpe/Calmar/drawdown/turnover expectations. | — | — | — | — |
| Validation | ✅ done | Compare errors/performance vs challenger models. | ✅ done | Compare base vs stacked performance. | ✅ pass | — |
| Risk | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ pass | — |
| Reports | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ pass | — |
| Monitor / Telemetry | ✅ done | Create monitor with PSI/KS diagnostics. | ✅ done | 🟠 Integrate PSI/KS drift diagnostics into monitoring flow. | ✅ pass | — |
| Compliance | ✅ done | 🟠 Expand `compliance.md` with SEC/ESMA references and research-mode policy. | — | — | ✅ pass | — |
| Infra | ✅ done | Standardize CLI entry, render, config, env. | ✅ done | Standardize CLI entry, render, config, env. | ✅ pass | — |
| Decisions | — | — | ✅ done | Dashboard_production_plan_spec authored. | 🟡 planning | 🟠 Finalize `decisions/dashboard_production_plan_spec.md` and add PR-traceable decision logging workflow. |
| Packs | — | — | ✅ done | 🟠 Prepare/document release candidate `packs/releases/v1.0-rc` (models, configs, reports, changelog). | — | — |

## Outstanding items at a glance

- **V1 carry-overs:** complete the outstanding data validation, table refactor, and backtest parameterization items that remained open when V1 was archived. These are captured in the V1 checklist YAML and still serve as historical gaps.【F:docs/tracking/phoenix_checklist.yaml†L6-L45】
- **V2 follow-ups:** synthetic data stream support, drift diagnostics integration, model output consolidation, and the v1.0-rc pack preparation are explicitly flagged for V2 and remain the key asks raised in that review.【F:docs/tracking/phoenix_checklist_v2.yaml†L7-L52】
- **V3 planning:** the dashboard production plan specification is still in planning status and requires decision logging with PR traceability before the V3 review can be considered complete.【F:docs/tracking/phoenix_checklist_v3.yaml†L1-L16】
