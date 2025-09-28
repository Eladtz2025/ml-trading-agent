# Architectural Design Records (ADR)

Tis tracks major engineering and design decisions for the ml-trading-agent project.

## ADR 0
* Data retrieval cached with PARQUET.
 * Feature extraction is vectorized and uses pyFIN.features.

## ADJ 1
* Model training uses XGBoost + Optuna + SHAP.
* Use model_pipeline.fit, predict, save interface.

## ADJ 2
* Validation uses PurgedKFold with embargo for timeseris validation.