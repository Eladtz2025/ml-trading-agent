# VVV Entry Monitor

A deliberately small, alert-only monitor for Venice Token (VVV).

It does **not** place real trades. Its job is to answer one question:

> Has VVV stopped falling and produced a sufficiently clean 1H long-entry
> structure to justify attention?

## Data

The monitor reads **closed 1-hour VVVUSDT perpetual candles** from Binance
USD-M Futures. The pair has existed on Binance Futures since January 2025.

The current unfinished candle is ignored.

## Entry rule

An entry is marked `ENTRY_READY` only when all of these are true:

1. A confirmed local low exists.
2. Price bounced at least 3% from that low.
3. A later confirmed low is higher than the first low.
4. Price closes above the swing high between those two lows.
5. Price is above the 20-period EMA.
6. Breakout volume is at least the prior 20-hour average.
7. Price is no more than 3% above the breakout level, so the monitor does not
   chase an already-extended move.
8. With the selected leverage, the structural invalidation does not exceed
   the configured maximum account-risk allowance.

The default example matches the conversation assumptions:

- Capital: $10,000
- Leverage: 3x
- Notional exposure: $30,000
- Maximum modeled capital loss to structural invalidation: 20%

## Structural invalidation

The bottom thesis is treated as invalid below the first confirmed low, with a
0.5% buffer.

This is **not** a liquidation calculator and does not replace the exchange's
actual liquidation price, maintenance-margin rules, fees, slippage, or funding.

## Statuses

- `NEED_MORE_DATA`: not enough closed 1H candles.
- `WAITING_FOR_STRUCTURE`: no clean low -> bounce -> higher-low pattern.
- `WAITING_FOR_BREAKOUT`: higher low exists; swing high has not been reclaimed.
- `WAITING_FOR_MOMENTUM`: breakout exists but price is not above EMA20.
- `WAITING_FOR_VOLUME`: breakout volume is not confirmed.
- `WAIT_FOR_PULLBACK`: valid breakout, but price is already too extended.
- `RISK_TOO_WIDE`: technical setup is valid, but 3x makes the structural
  invalidation too expensive.
- `ENTRY_READY`: all gates pass.

## Run

From the repository root:

```bash
python -m vvv_monitor.cli
```

For machine-readable output:

```bash
python -m vvv_monitor.cli --json
```

Different capital or leverage:

```bash
python -m vvv_monitor.cli --capital 5000 --leverage 2
```

## Design choice

The monitor intentionally reuses only the useful ideas from the older trading
systems: confirmed pullback/reversal structure, EMA20, volume confirmation,
explicit invalidation, risk visibility, and testable rules.

It intentionally excludes broad coin scanning, ML scores, BTC-regime scores,
prediction-market logic, automatic execution, and other layers that do not
help answer the VVV entry question.
