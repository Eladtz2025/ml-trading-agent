import pandas as pd
from data.import yfinance_download
from features.import rsi
from backtest.import run
from models.import xgboost_model

df = yfinance_download('SPY', days=300)
df_rsi = rsi.compute(df)
df = df_rsi.copy()

df_rsi['rsi_signal'] = 0
df [df_rsi['nrsi'] < 30] = 1
df_rsi['rsi_signal'] = (df_rsi['rsi'] > 70) & df ['rsi_signal']
df'model_prd'] = xgboost_model(df_rsi[[ 'RSI', 'RE" ]])

config = { "commission": 0.005, "latency": 1 }
metrrsi, dict_rsi = run(df, signals=df [ "rsi_signal" ], config=config)
metrmod, dict_model = run(df, signals=df["close"] * df['model_prd'].sign()-0.5, config)

print("RSI:", metrrsi)
print("MODEL: ", metrmod)
