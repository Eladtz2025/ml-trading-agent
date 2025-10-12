# Compliance Overview - ML Trading Agent

This document provides a summary of the regulatory guardrails that govern the Phoenix research program. It is not legal advice; engage qualified counsel before deploying to production.

## Regulatory References

### United States (SEC / FINRA)
- **Regulation NMS / Best Execution** – monitor routing quality and publish venue statistics.
- **Market Manipulation Controls** – document surveillance and kill-switch procedures.
- **Record Keeping (SEC Rule 17a-4)** – archive model configs, decisions, and experiment outputs for seven years.

### European Union & United Kingdom (ESMA / FCA)
- **MiFID II & MiFIR** – retain trade reconstruction data and maintain algorithmic trading self-assessments.
- **Market Abuse Regulation** – enforce controls that detect spoofing/quote stuffing prior to any live deployment.
- **Operational Resilience** – document disaster recovery for model hosting and data pipelines.

## Research-Only Controls
- All experiments must run with the `research_mode=true` flag in configurations and dashboards.
- Every generated report must include the disclaimer: _“For research purposes only. Not investment advice.”_
- Synthetic data streams must be labelled clearly; no live routing without compliance approval.

## Required Artefacts
- Maintain an up-to-date `compliance/audit_log.py` export for regulatory review.
- Ensure every PR references the applicable control in `decisions/` via the decision logging workflow.
- File quarterly compliance attestations covering data lineage, model risk, and monitoring efficacy.
