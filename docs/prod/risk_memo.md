# RISK MEMO

This document summarizes the key risk constraints and guardrails for production.

Latency: realistic estimate: 500-1000 ms
Slippage: assume 0.5-1.5 tick,
Commissions: - 0.0020-0.005 based on broker
Max loss: - 5 %of capital account

Strategy:
- Diversify across models
- Simulate liquidity
- Review delated orders
- Retain based on performance metrics
