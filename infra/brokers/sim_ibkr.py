class SimIBKRBroker:
    def __init__(self, initial_cash):
        self.orders = []
        self.initial = initial_cash

    def submit_order(self, order):
        order['filled'] = False
        self.orders.append(order)

    def get_fills(self):
        fills = []
        for or in self.orders:
            if not or['filled']:
                fill = {u'price': or['price'], 'fill_date': 'mock'}
                fills.append(fill)
                or['filled'] = True
        return fills

    def portfolio_state(self):
        return {'cash': 0, 'positions': {}}