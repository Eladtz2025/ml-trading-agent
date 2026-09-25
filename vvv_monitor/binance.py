from __future__ import annotations

import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .core import Candle

FUTURES_BASE_URL = "https://fapi.binance.com"


def fetch_closed_klines(
    *,
    symbol: str = "VVVUSDT",
    interval: str = "1h",
    limit: int = 200,
    base_url: str = FUTURES_BASE_URL,
    timeout: float = 10.0,
    now_ms: int | None = None,
) -> list[Candle]:
    """Fetch only fully closed Binance USD-M futures candles."""

    if not 1 <= limit <= 1500:
        raise ValueError("Binance kline limit must be between 1 and 1500")

    query = urlencode(
        {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
    )
    url = f"{base_url.rstrip('/')}/fapi/v1/klines?{query}"
    request = Request(
        url,
        headers={"User-Agent": "vvv-entry-monitor/1.0"},
    )

    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    clock_ms = now_ms if now_ms is not None else int(time.time() * 1000)

    candles: list[Candle] = []
    for row in payload:
        close_time_ms = int(row[6])
        if close_time_ms >= clock_ms:
            continue

        candles.append(
            Candle(
                open_time_ms=int(row[0]),
                close_time_ms=close_time_ms,
                open=float(row[1]),
                high=float(row[2]),
                low=float(row[3]),
                close=float(row[4]),
                volume=float(row[5]),
            )
        )

    return candles
