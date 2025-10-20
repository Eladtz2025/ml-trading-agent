from agent.context_provider import ContextProvider

class PhoenixAgent:
    def __init__(self):
        self.ctx = ContextProvider()

    def process(self, query: str) -> str:
        context = self.ctx.get_context()
        if "why" in query.lower():
            decision = context["last_decision"]
            action = decision["action"]
            asset = decision["asset"]
            confidence = decision["confidence"]
            expl = f"I decided to {action} {asset} because model confidence was {confidence}."
            expl += " Top feature: RSI."
            return expl
        elif "pnl" in query.lower():
            return f@"Current PnL is {(context['portfolio']['pnl')}"
        else:
            return "I'm ready. Ask me about recent decisions or performance."
