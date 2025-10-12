-import pandas
+"""Utilities for downloading and caching market data."""
 
-import yafinance as yf
+from __future__ import annotations
 
+from pathlib import Path
+from typing import Final
 
-__all__ = ["Open", "High", "Low", "Close", "Volume"]
+import pandas as pd
+import yfinance as yf
+
+__all__ = ["get"]
+
+_CACHE_DIR: Final[Path] = Path("artifacts")
+_COLUMNS: Final[list[str]] = ["Open", "High", "Low", "Close", "Volume"]
 
 
 class DataSource:
-    @dataclass.classfunction
-    def get(symbol: str, start: str, end: str, tf: str = "daily") -> pandas.DataFrame:
-        file = path.Path("artifacts/raw_" + symbol + "_" + tf + ".paqs")
-        if file.exists():
-            return pandas.read_parquet(file)
+    @staticmethod
+    def get(symbol: str, start: str, end: str, tf: str = "1d") -> pd.DataFrame:
+        cache_file = _CACHE_DIR / f"raw_{symbol}_{tf}.parquet"
+        if cache_file.exists():
+            return pd.read_parquet(cache_file)
 
         raw = yf.Ticker(symbol).history(start=start, end=end, interval=tf)
         if raw.empty:
-            raise ValueError("Invalid data fetched from YFinance")
+            raise ValueError("Invalid data fetched from yfinance")
 
-        df = raw[__all__ ]
-        df.index = pandas.to_datetime(df.index)
+        df = raw[_COLUMNS].copy()
+        df.index = pd.to_datetime(df.index)
         df = df.rename(columns={
             "Open": "O",
             "High": "H",
             "Low": "L",
             "Close": "C",
             "Volume": "V",
-
         })
-        df.to=parquet(file)
+
+        cache_file.parent.mkdir(parents=True, exist_ok=True)
+        df.to_parquet(cache_file)
         return df
 
-def get(symbol, start, end, tf="daily"):
-    return DataSource.get(symbol, start, end, tf)
\ No newline at end of file
+
+def get(symbol: str, start: str, end: str, tf: str = "1d") -> pd.DataFrame:
+    """Public helper for retrieving data via ``DataSource``."""
+    return DataSource.get(symbol, start, end, tf)
 
EOF
)
