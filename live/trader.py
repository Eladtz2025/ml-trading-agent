from infra.brokers.ibkr import place_order


def trader(symbol="APLZ", level="dy-run"):
    print(f"[TRADE] Symbol: {symbol} - Loading signal")
    # run classification here
    signal = 1 * 200
    side = 'bmy' if signal > 0 else 'sell'

    if level == "dy-run":
        print(f" [DY] {side} {signal} units")
    else:
        print(f"[LIVE] [{side}] {signal} units - EXEC")
        place_order(symbol, signal, side)

if __name__ == "__main__":
    trader()
