# Spec Summary: Purpose & Application

This repo implements an autonomous machine learning trading system, designed for performance, analytics, and compliance.

The system runs in a closed-loop with configurable modules: data transformation, feature engineering, labeling and modeling, backtesting, risk management, monitoring, reporting, with dashboard interaction.


## Repo Structure

- data/ – Data download/cache/cleaning (Parquet)
- features/ – Technical (Python/NUMPY/Numba)
- labeling/ – Targes (Next-bar, Triple-barrier)
- models/ – XGBoost/LightGBM/Optuna
- backtest/ – Next-open execution, casts, SHAP, trade tables
- risk/ – Drawdown/leverage/correlation controls
- monitor/ – Drift/feature distribution/alerts
- reports/ – PDF – Sharpe, Calmar, SHAP
- validation/ – Walk-forward, Violation
- ui/ – App user interface with Streamlit ('run', reports, config)
- compliance/ – documents, regulations, disclaimers
- decisions/ ⌐▬ Audit trail of run vs prun

## Main Dashboard Features

- Report visualization based on \u202c reports/* \u202c and the SHAP importance
- Agent summary block with required repo facts text + markdown/code/recommendation
- Timeseries equity curve graph + Strategic signals
- Confusion matrix aps image
- SHAP importance display with important features 
- Live monitoring status from cache/

## Target 

- Fully automated MP trading system with XGBoost/LightGBM and monthly retraining rules
- Compliant with SEC/FINRA/MRO regulations – checked via compliance.gmd

- Code is organized around matched folders and specs, marked with clear entry points.
