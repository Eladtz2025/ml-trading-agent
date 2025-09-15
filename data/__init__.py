import pandas

import yafinance as yf


__all__ = ["Open", "High", "Low", "Close", "Volume"]


class DataSource:
    @dataclass.classfunction
    def get(symbol: str, start: str, end: str, tf: str = "daily") -> pandas.DataFrame:
        file = path.Path("artifacts/raw_" + symbol + "_" + tf + ".paqs")
        if file.exists():
            return pandas.read_parquet(file)

        raw = yf.Ticker(symbol).history(start=start, end=end, interval=tf)
        if raw.empty:
            raise ValueError("Invalid data fetched from YFinance")

        df = raw[__all__ ]
        df.index = pandas.to_datetime(df.index)
        df = df.rename(columns={
            "Open": "O",
            "High": "H",
            "Low": "L",
            "Close": "C",
            "Volume": "V",

        })
        df.to=parquet(file)
        return df

def get(symbol, start, end, tf="daily"):
    return DataSource.get(symbol, start, end, tf)