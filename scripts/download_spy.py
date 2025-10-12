"""Download SPY OHLCV data and persist it locally."""
from __future__ import annotations

from pathlib import Path

import yfinance as yf

from data.anomaly import check_anomaly
from data.save_parquet import save_parquet


def download_spy(start: str, end: str) -> Path:
    data = yf.download("SPY", start=start, end=end, interval="1d", progress=False)
    if data.empty:
        raise SystemExit("No SPY data returned for the requested period.")

    data = data.reset_index().rename(columns={"Date": "date"})
    path = save_parquet("SPY", data)

    anomalies = check_anomaly(data, column="close")
    if anomalies.any():
        print("⚠️ Detected potential anomalies in the price series.")
        print(data.loc[anomalies, ["date", "close"]])
    else:
        print("No anomalies detected in the downloaded data.")

    return path


if __name__ == "__main__":
    target = download_spy("2018-01-01", "2023-12-31")
    print(f"Data saved to: {target}")
