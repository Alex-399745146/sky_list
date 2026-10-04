# tests/test_analytics.py
"""Тесты фильтрации и сортировки самолётов."""

from typing import Any

import pytest

from src.analytics import filter_aeroplanes_by_keyword, sort_aeroplanes


@pytest.fixture()
def aeroplanes_data() -> list[dict[str, Any]]:
    """Возвращает набор данных самолётов для аналитических тестов."""
    return [
        {
            "callsign": "UAE41P",
            "reg_country": "United Arab Emirates",
            "velocity": 73.14,
            "altitude": 68.58,
        },
        {
            "callsign": "GFA2004",
            "reg_country": "Bahrain",
            "velocity": 555.57,
            "altitude": 4145.28,
        },
        {
            "callsign": "FAD437",
            "reg_country": "Saudi Arabia",
            "velocity": 139.49,
            "altitude": 1569.72,
        },
    ]


def test_filter_aeroplanes_by_country_keyword(
    aeroplanes_data: list[dict[str, Any]],
) -> None:
    """Проверяет поиск по части названия страны без учёта регистра."""
    result = filter_aeroplanes_by_keyword(aeroplanes_data, "arab")

    assert len(result) == 2
    assert {plane["reg_country"] for plane in result} == {
        "United Arab Emirates",
        "Saudi Arabia",
    }


def test_filter_aeroplanes_by_callsign_keyword(
    aeroplanes_data: list[dict[str, Any]],
) -> None:
    """Проверяет поиск по части позывного."""
    result = filter_aeroplanes_by_keyword(aeroplanes_data, "gfa")

    assert len(result) == 1
    assert result[0]["callsign"] == "GFA2004"


def test_filter_aeroplanes_returns_all_for_empty_keyword(
    aeroplanes_data: list[dict[str, Any]],
) -> None:
    """Проверяет, что пустой запрос возвращает все записи."""
    result = filter_aeroplanes_by_keyword(aeroplanes_data, "")

    assert result == aeroplanes_data
    assert result is not aeroplanes_data


def test_sort_aeroplanes_by_altitude_descending(
    aeroplanes_data: list[dict[str, Any]],
) -> None:
    """Проверяет сортировку по высоте от большей к меньшей."""
    result = sort_aeroplanes(
        aeroplanes_data,
        sort_by="altitude",
        reverse=True,
    )

    assert [plane["callsign"] for plane in result] == [
        "GFA2004",
        "FAD437",
        "UAE41P",
    ]


def test_sort_aeroplanes_by_velocity_ascending(
    aeroplanes_data: list[dict[str, Any]],
) -> None:
    """Проверяет сортировку по скорости от меньшей к большей."""
    result = sort_aeroplanes(
        aeroplanes_data,
        sort_by="velocity",
    )

    assert [plane["callsign"] for plane in result] == [
        "UAE41P",
        "FAD437",
        "GFA2004",
    ]


def test_sort_aeroplanes_raises_for_invalid_field() -> None:
    """Проверяет ошибку для неподдерживаемого поля сортировки."""
    with pytest.raises(ValueError, match="Неподдерживаемое поле сортировки"):
        sort_aeroplanes([], sort_by="reg_country")
