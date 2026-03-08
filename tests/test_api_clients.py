# test_api_clients.py

import requests
import pytest

@pytest.mark.parametrize("url, order_codes", [
    ("https://httpbin.org/status/200", [200]),
    ("https://opensky-network.org", [200, 403]),
    ("https://nominatim.openstreetmap.org", [200, 403]),
])
def test_multiple_api_nodes(url, order_codes):
    """Параметризованный тест для проверки нескольких API‑узлов"""
    try:
        response = requests.get(url, timeout=10)
        assert response.status_code in order_codes, (
            f"Узел {url} вернул статус: {response.status_code}. "
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Не удалось подключиться к {url}: {e}")

