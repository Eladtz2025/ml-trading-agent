# Compliance Overview - ML Trading Agent

This document provides a summary of the regulatory guardrails that govern the Phoenix research program. It is not legal advice; engage qualified counsel before deploying to production.

## Regulatory References

### United States (SEC / FINRA)
- **Regulation NMS / Best Execution** – monitor routing quality and publish venue statistics.
- **Market Manipulation Controls** – document surveillance and kill-switch procedures.
- **Record Keeping (SEC Rule 17a-4)** – archive model configs, decisions, and experiment outputs for seven years.
- **Market Access Rule (SEC Rule 15c3-5)** – certify pre-trade risk checks limit erroneous or destabilising orders.
- **Regulation SCI / Cybersecurity** – demonstrate resilience and incident response for material system outages.

### European Union & United Kingdom (ESMA / FCA)
- **MiFID II & MiFIR** – retain trade reconstruction data and maintain algorithmic trading self-assessments.
- **Market Abuse Regulation** – enforce controls that detect spoofing/quote stuffing prior to any live deployment.
- **Operational Resilience** – document disaster recovery for model hosting and data pipelines.
- **ESMA Supervisory Briefing (ESMA35-36-1210)** – align algorithmic trading testing with the prescribed kill-switch and throttling standards.
- **FCA FG16/5** – ensure governance boards review and approve material model updates prior to live activation.

## Research-Only Controls
- All experiments must run with the `research_mode=true` flag in configurations and dashboards.
- Every generated report must include the disclaimer: _“For research purposes only. Not investment advice.”_
- Synthetic data streams must be labelled clearly; no live routing without compliance approval.
- Access to live brokerage credentials is gated behind compliance sign-off recorded in `compliance/audit_log.py`.
- Research environments must isolate production identifiers and anonymise counterparties; only aggregated statistics may exit the sandbox.

## Required Artefacts
- Maintain an up-to-date `compliance/audit_log.py` export for regulatory review.
- Ensure every PR references the applicable control in `decisions/` via the decision logging workflow.
- File quarterly compliance attestations covering data lineage, model risk, and monitoring efficacy.
- Capture evidence of ESMA RTS 6 testing runs (latency, kill-switch, capacity) within the monitoring artefacts produced by `monitoring/`.
