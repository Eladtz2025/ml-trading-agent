# Architecture Blueprint

This document presents the master architecture for the Phoenix Trading Agent.
 - Real-time streams, low latency, high thruput
Requirements:
- Real-time response in ticks (<100 ms)
- Reproducible events with custom handlers
- Able to support multiple trading strategies
- Create and update real-time features
- Support running via ML models with feature composition
- Enforce time-zone consistency
- Support retrain, re-tune with drift knowledge
