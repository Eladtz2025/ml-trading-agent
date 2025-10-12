# Phoenix Checklist Summary

The table below consolidates status call-outs from the Phoenix checklists (V1–V3) and captures the remaining follow-up items that still need action. “—” indicates that the item was not tracked for that version. Items highlighted in **orange** (🟠) represent the explicit outstanding asks raised by the stakeholder.

| Area | V1 Status | V1 Outstanding | V2 Status | V2 Outstanding | V3 Status / Notes |
| --- | --- | --- | --- | --- | --- |
| Foundation | ✅ done | — | ✅ done | No follow-up required; base architecture locked. | ✅ pass |
| Data | ✅ done | ✅ Fee quality validation + anomaly detection implemented (`data/fees_quality.py`). | ✅ done | ✅ Synthetic stream tags + live ingestion manager delivered (`data/live.py`). | ✅ pass |
| Features | ✅ done | ✅ MACD/ATR plugins refactored with regression tests. | ✅ done | ✅ PSI/KS drift diagnostics integrated via `monitoring/`. | ✅ pass |
| Labeling | ✅ done | ✅ Confidence scoring + long-horizon thresholds implemented (`labeling/confidence.py`). | ✅ done | ✅ Confidence scoring reused for V2. | ✅ pass |
| Models / Prediction | ✅ done | Stacked ML@+LGBM upgrade landed. | ✅ done | ✅ Consolidated signal/return export + metadata logging (`models/output.py`, `models/model_io.py`). | ✅ pass |
| Backtest | ✅ done | ✅ Latency, slippage, capital parameterization shipped (`backtest/core.py`). | ✅ done | ✅ Next-bar open fill logic verified via tests. | ✅ pass |
| Tables | ✅ done | ✅ Summary statistics table aligned to Sharpe/Calmar/drawdown/turnover (`reports/metrics_table.py`). | — | — | — |
| Validation | ✅ done | Compare errors/performance vs challenger models. | ✅ done | Compare base vs stacked performance. | ✅ pass |
| Risk | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ done | Dynamic capital logic + correlation limits documented. | ✅ pass |
| Reports | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ done | Generate SHAP plots, custom metrics, equity curves → PDF/HTML. | ✅ pass |
| Monitor / Telemetry | ✅ done | Create monitor with PSI/KS diagnostics. | ✅ done | ✅ Integrated PSI/KS drift diagnostics (`monitoring/drift.py`). | ✅ pass |
| Compliance | ✅ done | ✅ `compliance.md` expanded with SEC/ESMA references and research-mode policy. | — | — | ✅ pass |
| Infra | ✅ done | Standardize CLI entry, render, config, env. | ✅ done | Standardize CLI entry, render, config, env. | ✅ pass |
| Decisions | — | — | ✅ done | Dashboard_production_plan_spec authored. | ✅ Spec finalized + decision logging workflow (`decisions/dashboard_production_plan_spec.md`, `decisions/log.py`). |
| Packs | — | — | ✅ done | ✅ Release candidate `packs/releases/v1.0-rc` documented (models, configs, reports, changelog). | — |
