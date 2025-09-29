# Architectural Design Records (ADR)

This tracks major engineering and design decisions for the ml-trading-agent project.

## ADR Coverage
* Data retrieval cached with PARQUET.
* Feature extraction via pyFIN.features.
* Model training uses XGBoost + Optuna + SHAP.

## ADR 0
* Research init with RSI threshold test.
* Data retrieval cached with PARQUET.
* Feature extraction is vectorized and uses pyFIN.features.

## ADR 1
* Model training uses XGBoost with simple fixed params.
* Model training uses XGBoost + Optuna + SHAP.
* Use model_pipeline.fit, predict, save interface.

## ADR 2
* Validation uses PurgedKFold with embargo for time-series validation.

## ADR 3
* Labeling function: sign(close_[t+3] - close_t)
* Used for binary classification on three-lagspan price direction.
* Suppresses returns below 0.002 range.