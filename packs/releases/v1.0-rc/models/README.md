# Models

The serialized estimators and metadata exported via `models/output.py` should be dropped into this directory. Include:

- `signals_returns.parquet`
- `signals_returns.metadata.json`
- `model_<version>.pkl`
- `model_<version>.json`

For this RC package the files are generated automatically by the deployment pipeline and attached during promotion.
