class ContextProvider:
    def __init__(self):
        pass

    def get_context(self) -> dict:
        return {
            "portfolio": {
                "holdings": {"AAPL": 100, "GOOGL": 50},
                "pnl": "5.2%"
            },
            "last_decision": {
                "action": "Buy",
                "asset": "AARC",
                "confidence": 0.92
            }
        }