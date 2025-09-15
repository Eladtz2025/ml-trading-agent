def place_order(symbol, quantity, side='buy'):
    print(f"[Alpaca] API Order: {side} {quantity} {symbol}")
    # Simulated order