# test_api_clients.py
"""Тест кейсы проверки модуля работы с API"""

import pytest
import requests

import src.api_clients as api_clients
from src.api_clients import APIAdapter


@pytest.mark.parametrize(
    "url, order_codes",
    [
        ("https://httpbin.org/status/200", [200]),
        ("https://opensky-network.org", [200, 403]),
        ("https://nominatim.openstreetmap.org", [200, 403]),
    ],
)
def test_multiple_api_nodes(url, order_codes):
    """Параметризованный тест для проверки нескольких API‑узлов"""
    try:
        response = requests.get(url, timeout=10)
        assert response.status_code in order_codes, f"Узел {url} вернул статус: {response.status_code}. "
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Не удалось подключиться к {url}: {e}")


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data


def test_api_clients(monkeypatch) -> None:
    """Проверка работы APIAdapter с замоканными запросами к двум API."""

    url_map = APIAdapter().url_map
    url_sky = APIAdapter().url_sky

    def mock_get(url, params=None, headers=None, timeout=10):
        if url == url_map:
            return MockResponse(
                json_data=[
                    {"boundingbox": ["10.0", "20.0", "30.0", "40.0"]},
                ],
                status_code=200,
            )
        if url == url_sky:
            return MockResponse(
                json_data={"states": [["plane1"], ["plane2"]]},
                status_code=200,
            )
        return MockResponse(json_data={}, status_code=400)

    # патчим именно функцию get, импортированную в модуле src.api_clients
    monkeypatch.setattr(api_clients, "get", mock_get)

    adapter = APIAdapter()
    adapter.get_aeroplanes("Russia")  # метод сам положит данные во внутренний атрибут

    data = adapter.aeroplanes
    assert isinstance(data, dict)
    assert "states" in data
    assert len(data["states"]) == 2
