from __future__ import annotations

from vvv_monitor.core import Candle, MonitorConfig, evaluate

HOUR = 3_600_000


def candle(
    i: int,
    open_price: float,
    high: float,
    low: float,
    close: float,
    volume: float = 100.0,
) -> Candle:
    return Candle(
        open_time_ms=i * HOUR,
        close_time_ms=(i + 1) * HOUR - 1,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def prefix(count: int = 24) -> list[Candle]:
    bars: list[Candle] = []
    price = 110.0
    for i in range(count):
        bars.append(
            candle(
                i,
                price,
                price + 1.0,
                price - 1.0,
                price - 0.2,
            )
        )
        price -= 0.15
    return bars


def reversal_bars(
    *,
    breakout_close: float = 106.2,
    breakout_volume: float = 160.0,
) -> list[Candle]:
    bars = prefix()
    i = len(bars)

    bars += [
        candle(i, 103, 104, 101, 102, 100),
        candle(i + 1, 102, 103, 100, 101, 110),
        candle(i + 2, 101, 103, 101, 102.5, 105),
        candle(i + 3, 102.5, 106, 103.5, 105.5, 120),
        candle(i + 4, 105.5, 105.8, 103.0, 104, 95),
        candle(i + 5, 104, 104.5, 102.2, 103, 90),
        candle(i + 6, 103, 104.2, 102.6, 103.8, 95),
        candle(i + 7, 103.8, 105.5, 103.2, 105, 100),
        candle(
            i + 8,
            105,
            max(106.2, breakout_close + 0.1),
            104.5,
            breakout_close,
            breakout_volume,
        ),
    ]
    return bars


def test_entry_ready_after_higher_low_breakout_volume_and_ema() -> None:
    result = evaluate(
        reversal_bars(),
        MonitorConfig(max_account_risk_pct=0.30),
    )

    assert result.status == "ENTRY_READY"
    assert result.first_low == 100
    assert result.higher_low == 102.2
    assert result.breakout_level == 106
    assert result.volume_ratio is not None
    assert result.volume_ratio >= 1.0
    assert result.entry_price == 106.2
    assert result.invalidation_price == 99.5


def test_waits_before_breakout() -> None:
    result = evaluate(
        reversal_bars(breakout_close=106.0),
        MonitorConfig(max_account_risk_pct=0.30),
    )
    assert result.status == "WAITING_FOR_BREAKOUT"


def test_rejects_weak_breakout_volume() -> None:
    result = evaluate(
        reversal_bars(breakout_volume=50.0),
        MonitorConfig(max_account_risk_pct=0.30),
    )
    assert result.status == "WAITING_FOR_VOLUME"


def test_does_not_chase_far_above_breakout() -> None:
    result = evaluate(
        reversal_bars(
            breakout_close=110.0,
            breakout_volume=180.0,
        ),
        MonitorConfig(max_account_risk_pct=0.50),
    )
    assert result.status == "WAIT_FOR_PULLBACK"


def test_blocks_entry_when_structural_risk_is_too_wide() -> None:
    result = evaluate(
        reversal_bars(),
        MonitorConfig(
            leverage=3.0,
            max_account_risk_pct=0.10,
        ),
    )

    assert result.status == "RISK_TOO_WIDE"
    assert result.account_risk_pct is not None
    assert result.account_risk_pct > 0.10
