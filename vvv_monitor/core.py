from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class Candle:
    open_time_ms: int
    close_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class MonitorConfig:
    pivot_wing: int = 2
    lookback_bars: int = 96
    min_bounce_pct: float = 0.03
    min_higher_low_pct: float = 0.003
    max_higher_low_pct: float = 0.15
    breakout_buffer_pct: float = 0.001
    max_chase_pct: float = 0.03
    volume_window: int = 20
    min_volume_ratio: float = 1.0
    ema_window: int = 20
    stop_buffer_pct: float = 0.005
    capital_usd: float = 10_000.0
    leverage: float = 3.0
    max_account_risk_pct: float = 0.20


@dataclass(frozen=True)
class MonitorResult:
    status: str
    reason: str
    current_price: float
    support: float | None = None
    first_low: float | None = None
    higher_low: float | None = None
    breakout_level: float | None = None
    ema20: float | None = None
    volume_ratio: float | None = None
    entry_price: float | None = None
    invalidation_price: float | None = None
    target_1r: float | None = None
    target_2r: float | None = None
    account_risk_usd: float | None = None
    account_risk_pct: float | None = None
    notional_usd: float | None = None
    signal_id: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _ema(values: Iterable[float], window: int) -> float:
    seq = list(values)
    if not seq:
        raise ValueError("EMA requires at least one value")

    alpha = 2.0 / (window + 1.0)
    value = seq[0]
    for item in seq[1:]:
        value = alpha * item + (1.0 - alpha) * value
    return value


def _pivot_lows(candles: list[Candle], wing: int) -> list[int]:
    result: list[int] = []
    for i in range(wing, len(candles) - wing):
        low = candles[i].low
        left = [candles[j].low for j in range(i - wing, i)]
        right = [candles[j].low for j in range(i + 1, i + wing + 1)]
        if low < min(left) and low <= min(right):
            result.append(i)
    return result


def _latest_valid_structure(
    candles: list[Candle],
    config: MonitorConfig,
) -> tuple[int, int, float] | None:
    lows = _pivot_lows(candles, config.pivot_wing)
    if len(lows) < 2:
        return None

    for pos in range(len(lows) - 1, 0, -1):
        l1 = lows[pos - 1]
        l2 = lows[pos]
        if l2 - l1 < 2:
            continue

        low1 = candles[l1].low
        low2 = candles[l2].low
        higher_low_pct = low2 / low1 - 1.0
        if not (
            config.min_higher_low_pct
            <= higher_low_pct
            <= config.max_higher_low_pct
        ):
            continue

        between = candles[l1 + 1 : l2]
        if not between:
            continue

        swing_high = max(candle.high for candle in between)
        if swing_high / low1 - 1.0 < config.min_bounce_pct:
            continue

        after_l2 = candles[l2 + 1 :]
        if after_l2:
            post_min = min(candle.low for candle in after_l2)
            if post_min <= low1:
                continue
            if post_min < low2 * (1.0 - 0.002):
                continue

        return l1, l2, swing_high

    return None


def evaluate(
    candles: list[Candle],
    config: MonitorConfig | None = None,
) -> MonitorResult:
    cfg = config or MonitorConfig()
    min_bars = max(
        cfg.ema_window + 2,
        cfg.volume_window + 2,
        cfg.pivot_wing * 2 + 8,
    )
    if len(candles) < min_bars:
        price = candles[-1].close if candles else 0.0
        return MonitorResult(
            status="NEED_MORE_DATA",
            reason=f"Need at least {min_bars} closed 1H candles.",
            current_price=price,
        )

    ordered = sorted(candles, key=lambda candle: candle.open_time_ms)
    window = ordered[-cfg.lookback_bars :]
    current = window[-1]

    ema_source = window[-max(cfg.ema_window * 4, cfg.ema_window) :]
    ema_value = _ema(
        (candle.close for candle in ema_source),
        cfg.ema_window,
    )

    baseline = window[-(cfg.volume_window + 1) : -1]
    baseline_volume = (
        mean(candle.volume for candle in baseline) if baseline else 0.0
    )
    volume_ratio = (
        current.volume / baseline_volume if baseline_volume > 0 else 0.0
    )

    structure = _latest_valid_structure(window, cfg)
    if structure is None:
        return MonitorResult(
            status="WAITING_FOR_STRUCTURE",
            reason="No confirmed low -> bounce -> higher-low structure yet.",
            current_price=current.close,
            ema20=ema_value,
            volume_ratio=volume_ratio,
        )

    l1, l2, breakout = structure
    low1 = window[l1].low
    low2 = window[l2].low

    breakout_trigger = breakout * (1.0 + cfg.breakout_buffer_pct)
    if current.close <= breakout_trigger:
        return MonitorResult(
            status="WAITING_FOR_BREAKOUT",
            reason=(
                "Higher low exists, but price has not closed above "
                "the swing high."
            ),
            current_price=current.close,
            support=low1,
            first_low=low1,
            higher_low=low2,
            breakout_level=breakout,
            ema20=ema_value,
            volume_ratio=volume_ratio,
        )

    if current.close > breakout * (1.0 + cfg.max_chase_pct):
        return MonitorResult(
            status="WAIT_FOR_PULLBACK",
            reason=(
                "Breakout is confirmed, but price is too far above "
                "the trigger to chase."
            ),
            current_price=current.close,
            support=low1,
            first_low=low1,
            higher_low=low2,
            breakout_level=breakout,
            ema20=ema_value,
            volume_ratio=volume_ratio,
        )

    if current.close <= ema_value:
        return MonitorResult(
            status="WAITING_FOR_MOMENTUM",
            reason="Breakout exists, but the close is not above EMA20.",
            current_price=current.close,
            support=low1,
            first_low=low1,
            higher_low=low2,
            breakout_level=breakout,
            ema20=ema_value,
            volume_ratio=volume_ratio,
        )

    if volume_ratio < cfg.min_volume_ratio:
        return MonitorResult(
            status="WAITING_FOR_VOLUME",
            reason=(
                "Breakout exists, but volume is below the 20-hour baseline."
            ),
            current_price=current.close,
            support=low1,
            first_low=low1,
            higher_low=low2,
            breakout_level=breakout,
            ema20=ema_value,
            volume_ratio=volume_ratio,
        )

    entry = current.close
    invalidation = low1 * (1.0 - cfg.stop_buffer_pct)
    if invalidation >= entry:
        return MonitorResult(
            status="WAITING_FOR_STRUCTURE",
            reason="Invalid structural geometry; no trade signal.",
            current_price=current.close,
            support=low1,
            first_low=low1,
            higher_low=low2,
            breakout_level=breakout,
            ema20=ema_value,
            volume_ratio=volume_ratio,
        )

    move_to_invalidation = (entry - invalidation) / entry
    account_risk_pct = move_to_invalidation * cfg.leverage
    account_risk_usd = cfg.capital_usd * account_risk_pct
    notional_usd = cfg.capital_usd * cfg.leverage

    risk_per_token = entry - invalidation
    target_1r = entry + risk_per_token
    target_2r = entry + 2.0 * risk_per_token
    signal_id = (
        f"{window[l1].open_time_ms}-"
        f"{window[l2].open_time_ms}-"
        f"{round(breakout, 6)}"
    )

    common = dict(
        current_price=current.close,
        support=low1,
        first_low=low1,
        higher_low=low2,
        breakout_level=breakout,
        ema20=ema_value,
        volume_ratio=volume_ratio,
        entry_price=entry,
        invalidation_price=invalidation,
        target_1r=target_1r,
        target_2r=target_2r,
        account_risk_usd=account_risk_usd,
        account_risk_pct=account_risk_pct,
        notional_usd=notional_usd,
        signal_id=signal_id,
    )

    if account_risk_pct > cfg.max_account_risk_pct:
        return MonitorResult(
            status="RISK_TOO_WIDE",
            reason=(
                "Technical entry confirmed, but structural invalidation "
                "risks too much capital at this leverage."
            ),
            **common,
        )

    return MonitorResult(
        status="ENTRY_READY",
        reason=(
            "Higher low + swing-high reclaim + EMA20 + "
            "volume confirmation."
        ),
        **common,
    )
