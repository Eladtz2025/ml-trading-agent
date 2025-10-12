# PIPELINE CONTRACTS

This document specifies the core functional interfaces for the ml-trading pipeline.

~** DataProvider.get(symbol, start, end, tf) => df
***Returns a Pandas DataFrame with columns: ["Open", "High", "Low", "Close", "Volume"]

** Feature.compute(df) => df
***For each feature function (rsi, macd, atr) return the same input frame with added column.

^* Model.train(X, y, config) => model
~** Model.predict(model, X) => z
***Model.save(model, path)

Models must support jit_save from within.

^* Backtest.run(df, signals, config) => metrics
**Engages the core simulation with costs and latency.