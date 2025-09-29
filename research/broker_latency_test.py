import time
from infra.brokers.sim_ibkr import SimIBKRBroker

broker = SimIBKRBroker()

durs = []

for _ in range(100):
    order = { 'sid': 'SPY', 'quantity': 10, 'price': 150, 'filled': False }
    st = time.time()
    broker.submit_order(order)
    fills = broker.get_fills()
    et = time.time()
    durs.append(et - st)

print("Latency sess:", sum(durs) / len(durs))
print("STDN:", pd.std(durs))