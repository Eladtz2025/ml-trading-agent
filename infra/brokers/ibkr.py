"""Convenience wrapper for routing orders to the simulated IBKR broker."""

from __future__ import annotations

from typing import Mapping, MutableMapping, Any

from .sim_ibkr import SimIBKRBroker

_DEFAULT_BROKER = SimIBKRBroker(initial_cash=100_000.0)


def _normalise_action(action: Mapping[str, Any]) -> dict:
    """Coerce an arbitrary mapping into the order format expected by the broker."""

    try:
        symbol = str(action["symbol"]).strip()
        quantity = int(action["quantity"])
        price = float(action["price"])
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise KeyError(f"Missing order field: {exc.args[0]}") from exc
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid order payload: unable to parse quantity or price") from exc

    if not symbol:
        raise ValueError("Order symbol cannot be empty")

    return {"symbol": symbol, "quantity": quantity, "price": price}


def execute(action: Mapping[str, Any] | MutableMapping[str, Any], broker: SimIBKRBroker | None = None) -> dict:
    """Submit an order to ``broker`` and return the resulting fill.

    The real project integrates with Interactive Brokers via their API.  For the
    purposes of unit tests and local experimentation we expose the same entry
    point while delegating execution to :class:`SimIBKRBroker`.  Callers can
    provide their own broker instance (for example, one instrumented in tests),
    otherwise a shared in-memory broker is used.
    """

    if broker is None:
        broker = _DEFAULT_BROKER

    if not isinstance(action, Mapping):
        raise TypeError("action must be a mapping of order fields")

    order = _normalise_action(action)
    broker.submit_order(order)
    fills = broker.get_fills()
    return fills[-1] if fills else {}


__all__ = ["execute", "SimIBKRBroker"]
