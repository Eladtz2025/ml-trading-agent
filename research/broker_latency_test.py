import time

from infra.brokers.sim_ibkr import SimIBKRBroker


def _measure_latency(iterations: int = 25) -> float:
    broker = SimIBKRBroker(initial_cash=10_000)
    durations = []

    for _ in range(iterations):
        start = time.perf_counter()
        broker.submit_order({"symbol": "SPY", "quantity": 1, "price": 150})
        broker.get_fills()
        durations.append(time.perf_counter() - start)

    return sum(durations) / len(durations)


def test_sim_ibkr_latency_is_small():
    latency = _measure_latency()
    assert latency < 0.001