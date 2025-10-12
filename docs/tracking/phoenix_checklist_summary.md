# Phoenix Checklist Summary

_Last reviewed: synchronized with_ `phoenix_checklist.yaml`, `phoenix_checklist_v2.yaml`, _and_ `phoenix_checklist_v3.yaml` _on 2025-10-12._

The table below consolidates the Phoenix checklist status across the three documented iterations. “—” indicates that the item was not tracked in that version.

| Area | V1 Status | V1 Outstanding | V2 Status | V2 Outstanding | V3 Status | V3 Outstanding |
| --- | --- | --- | --- | --- | --- | --- |
| Foundation | ✅ done | — | ✅ done | No follow-up required; base architecture locked. | ✅ pass | — |
| Data | ✅ done | — | ✅ done | — | ✅ pass | — |
| Features | ✅ done | — | ✅ done | — | ✅ pass | — |
| Labeling | ✅ done | — | ✅ done | — | ✅ pass | — |
| Models / Prediction | ✅ done | Stacked ML@+LGBM upgrade planned next. | ✅ done | — | ✅ pass | — |
| Backtest | ✅ done | — | ✅ done | — | ✅ pass | — |
| Tables | ✅ done | — | — | — | — | — |
| Validation | ✅ done | Compare errors/performance vs challenger models. | ✅ done | Compare base vs stacked performance. | ✅ pass | — |
| Risk | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ pass | — |
| Reports | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ pass | — |
| Monitor / Telemetry | ✅ done | Create monitor with PSI/KS diagnostics. | ✅ done | — | ✅ pass | — |
| Compliance | ✅ done | — | — | — | ✅ pass | — |
| Infra | ✅ done | Standardize CLI entry, render, config, env. | ✅ done | Standardize CLI entry, render, config, env. | ✅ pass | — |
| Decisions | — | — | ✅ done | Dashboard_production_plan_spec authored. | 🟡 planning | 🟠 Finalize `decisions/dashboard_production_plan_spec.md` and add PR-traceable decision logging workflow. |
| Packs | — | — | ✅ done | 🟠 Prepare/document release candidate `packs/releases/v1.0-rc` (models, configs, reports, changelog). | — | — |

## Outstanding items at a glance

- **V1 carry-overs:** resolved via the fee validation utilities, parameterised backtester, and refreshed metrics table implementation.【F:data/fees_quality.py†L12-L97】【F:backtest/core.py†L1-L66】【F:reports/metrics_table.py†L1-L44】
- **V2 follow-ups:** synthetic/live stream tagging, drift integration, model export consolidation, and compliance refresh have now landed in code and tests.【F:data/live.py†L1-L96】【F:monitoring/__init__.py†L1-L56】【F:models/output.py†L1-L47】【F:compliance/compliance.md†L1-L200】
- **V3 planning:** the dashboard production plan specification is still in planning status and requires decision logging with PR traceability before the V3 review can be considered complete.【F:docs/tracking/phoenix_checklist_v3.yaml†L1-L16】
