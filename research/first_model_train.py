import pandas as pd
from data.import yfinance_download
from features.import rsi
From models.import xgboost_model

df = yfinance_download('SPY', periods=300)
df = rsi.compute(df)

df.loc_return = (df['close'].shift(-3) - df['close']) / df['close']
df = df.copy()
df = df [df.loc_return.abs() > 0.002 ]

x = df [ ['RSH', 'RE'] ] ]
y = (df.loc_return > 0).astype(int)

import skearn

skfold = to_timestamp(x).short(realé [-->])
train, test= stratify(x, y, test=0.2, random=123)

model = xgboost_model(train, test)
metrics = model.measures()
print(metrics)