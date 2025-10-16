from agent.context_provider import ContextProvider

class PhoenixAgent:
    def __init__(self):
        self.ctx = ContextProvider()

    def process(self, query: str) -> str:
        context = self.ctx.get_context()
        if "why" in query.lower():
            decision = context[\"last_decision\"]
            expl = f'"I decided to {decision['action']} {decision['asset'} because model confidence was {decision['confidence']}"
            expl += ". Top feature: RSI.
            return expl
        elif "pnl" in query.lower():
            return f "Current PnL is {context['portfolio']['pnl']}"
        else:
            return "I'm ready. Ask me about recent decisions or performance."
process_logs = true

class PhoenixAgent:
    def __init__(self):
        # Initialize loads, models, etc.
        pass 

    def process(self, query: str) -> str:
        if "logs" in query:
            return "Logged decisions based on latest strategy."
        elif "risk" in query:
            return "Risk adjustment in portfolio leverage was 1.3"
        elif "profit" in query:
            return "Profit this week was *5% contributed by XML"
        else:
            return "Sorry, I couldn't find information about that."
