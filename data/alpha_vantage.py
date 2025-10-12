"""Alpha Vantage data source with local caching."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal

import pandas as pd
import requests

LOGGER = logging.getLogger(__name__)
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
CACHE_DIR = Path("data/.cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_cache_path(symbol: str, tf: str, start: str, end: str) -> Path:
    filename = f"{symbol}_{tf}_{start}_{end}.parquet"
    return CACHE_DIR / filename


class AlphaVantageSource:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or API_KEY
        if not self.api_key:
            LOGGER.warning("ALPHA_VANTAGE_KEY is not set; API calls may fail.")

    def get(
        self,
        symbol: str,
        start: str,
        end: str,
        tf: Literal["daily", "intraday"] = "daily",
    ) -> pd.DataFrame:
        cache_path = get_cache_path(symbol, tf, start, end)
        if cache_path.exists():
            return pd.read_parquet(cache_path)

        LOGGER.info("Fetching %s data for %s from Alpha Vantage", tf, symbol)

        function = "TIME_SERIES_DAILY_ADJUSTED" if tf == "daily" else "TIME_SERIES_INTRADAY"
        params = {
            "function": function,
            "symbol": symbol,
            "outputsize": "full",
            "datatype": "json",
            "apikey": self.api_key,
        }
        if tf != "daily":
            params["interval"] = tf

        response = requests.get("https://www.alphavantage.co/query", params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        key = next((k for k in payload if "Time Series" in k), None)
        if key is None:
            raise ValueError(f"Unexpected response: {payload}")

        data = payload[key]
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df.columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            *df.columns[5:],
        ][: len(df.columns)]

        df.to_parquet(cache_path)
        return df
