from __future__ import annotations

import argparse
import json

from .binance import fetch_closed_klines
from .core import MonitorConfig, MonitorResult, evaluate


def _money(value: float | None) -> str:
    return "-" if value is None else f"${value:,.2f}"


def _pct(value: float | None) -> str:
    return "-" if value is None else f"{value * 100:.1f}%"


def format_human(result: MonitorResult) -> str:
    lines = [
        f"VVV STATUS: {result.status}",
        f"Current: {_money(result.current_price)}",
        f"Reason: {result.reason}",
    ]

    if result.first_low is not None:
        lines.extend(
            [
                f"Base low/support: {_money(result.first_low)}",
                f"Higher low: {_money(result.higher_low)}",
                f"Breakout level: {_money(result.breakout_level)}",
                f"EMA20: {_money(result.ema20)}",
                (
                    f"Volume ratio: {result.volume_ratio:.2f}x"
                    if result.volume_ratio is not None
                    else "Volume ratio: -"
                ),
            ]
        )

    if result.entry_price is not None:
        lines.extend(
            [
                f"Entry: {_money(result.entry_price)}",
                f"Invalidation: {_money(result.invalidation_price)}",
                f"Target 1R: {_money(result.target_1r)}",
                f"Target 2R: {_money(result.target_2r)}",
                f"Notional: {_money(result.notional_usd)}",
                (
                    "Capital at structural risk: "
                    f"{_money(result.account_risk_usd)} "
                    f"({_pct(result.account_risk_pct)})"
                ),
            ]
        )

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Minimal VVV 1H entry monitor"
    )
    parser.add_argument("--capital", type=float, default=10_000.0)
    parser.add_argument("--leverage", type=float, default=3.0)
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = MonitorConfig(
        capital_usd=args.capital,
        leverage=args.leverage,
    )
    candles = fetch_closed_klines(limit=args.limit)
    result = evaluate(candles, config)

    if args.as_json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_human(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
