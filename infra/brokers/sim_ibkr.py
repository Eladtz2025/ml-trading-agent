"""A tiny in-memory broker used for testing purposes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Order:
    symbol: str
    quantity: int
    price: float


class SimIBKRBroker:
    """Immediate fill broker that keeps track of cash and positions."""

    def __init__(self, initial_cash: float = 0.0):
        self.initial_cash = float(initial_cash)
        self.cash = float(initial_cash)
        self.positions: Dict[str, int] = {}
        self._pending_fills: List[dict] = []

    def submit_order(self, order: Dict) -> None:
        """Submit an order and fill it immediately."""

        try:
            symbol = order["symbol"]
            quantity = int(order["quantity"])
            price = float(order["price"])
        except KeyError as exc:
            raise KeyError(f"Missing required order field: {exc.args[0]}") from exc

        if quantity == 0:
            raise ValueError("Order quantity cannot be zero")

        self.cash -= quantity * price
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity

        fill = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
        }
        self._pending_fills.append(fill)

    def get_fills(self) -> List[dict]:
        fills, self._pending_fills = self._pending_fills, []
        return fills

    def portfolio_state(self) -> Dict[str, object]:
        return {
            "cash": self.cash,
            "positions": dict(self.positions),
            "initial_cash": self.initial_cash,
        }


__all__ = ["SimIBKRBroker", "Order"]
