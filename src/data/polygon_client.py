import os
import requests

def get_polygon_api_key():
    api_key = os.environ.get(
        "POLYGON_API_KEY")
    if not api_key:
        raise ValueError("Missing POLYGON_API_KEY in environment")
    return api_key

def get_splits(ticker: str, limit: int = 10):
    url = f"https://api.polygon.io/v3/reference/splits?ticker={ticker}&limit={limit}&apiKey={get_polygon_api_key()}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def get_dividends(ticker: str, limit: int = 10):
    url = f"https://api.polygon.io/v3/reference/dividends?ticker={ticker}&limit={limit}&apiKey={get_polygon_api_key()}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()