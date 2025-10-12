from src.data import polygon_client


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload
        self.called = False

    def raise_for_status(self):
        self.called = True

    def json(self):
        return self._payload


def test_get_splits_uses_api_key(monkeypatch):
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")

    response = DummyResponse({"results": []})
    urls = []

    def fake_get(url):
        urls.append(url)
        return response

    monkeypatch.setattr(polygon_client.requests, "get", fake_get)

    data = polygon_client.get_splits("AAPL", limit=5)

    assert response.called, "raise_for_status was not invoked"
    assert data == {"results": []}
    assert "AAPL" in urls[0]
    assert "splits" in urls[0]
    assert "limit=5" in urls[0]


def test_get_dividends_reuses_requests(monkeypatch):
    monkeypatch.setenv("POLYGON_API_KEY", "secret")

    response = DummyResponse({"results": [1]})

    def fake_get(url):
        return response

    monkeypatch.setattr(polygon_client.requests, "get", fake_get)

    data = polygon_client.get_dividends("MSFT", limit=1)

    assert data == {"results": [1]}