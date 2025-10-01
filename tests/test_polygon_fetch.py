from src.data.polygon_client import get_splits, get_dividends

if __name__ == "__main__":
    ticker = "AAPL"
    print("Fetching splits...")
    splits = get_splits(ticker)
    print(splits)

    print(\"\nFetching dividends...\")
    dividends = get_dividends(ticker)
    print(dividends)