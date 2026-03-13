# test_airplanes.py
"""Тест кейсы для классов обработки данных о самолётах"""

import pytest

from src.airplanes import Aeroplane


def test_init_object(fix_obj_aeroplane: Aeroplane, fix_init_aeroplane: dict) -> None:
    """Проверка создания объектов класса Aeroplane"""
    # Проверка атрибутов
    assert fix_obj_aeroplane.callsign == "BORT_007"
    assert fix_obj_aeroplane.reg_country == "Canada"
    assert fix_obj_aeroplane.velocity == 250.4
    assert fix_obj_aeroplane.altitude == 12545.5

    # Проверка инициализатора
    test_obj = Aeroplane(**fix_init_aeroplane)

    assert isinstance(test_obj, Aeroplane)

    assert test_obj.callsign == "BOING_001"
    assert test_obj.reg_country == "USA"
    assert test_obj.velocity == 200.5
    assert test_obj.altitude == 14444.5

    # Проверка типов данных
    assert isinstance(fix_obj_aeroplane.callsign, str)
    assert isinstance(fix_obj_aeroplane.reg_country, str)
    assert isinstance(fix_obj_aeroplane.velocity, float)
    assert isinstance(fix_obj_aeroplane.altitude, float)

    # Проверим методов
    result = test_obj.get_filter_aeroplanes(fix_init_aeroplane)
    assert isinstance(result, list)
    assert len(result) == 0
    assert result == []
    assert test_obj.__eq__(fix_obj_aeroplane) is False
    assert test_obj.__lt__(fix_obj_aeroplane) is False


def test_init_invalid_types_raises() -> None:
    """Проверка, что некорректные типы вызывают исключение."""
    with pytest.raises((TypeError, ValueError)):
        Aeroplane(1, "Canada", 250.4, 12545.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        Aeroplane("BORT_007", 1, 250.4, 12545.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        Aeroplane("BORT_007", "Canada", -345, 12545.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        Aeroplane("BORT_007", "Canada", 250.4, -2345.7)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        Aeroplane("BORT_007", "Canada", "123", 12545.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        Aeroplane("BORT_007", "Canada", 250.4, "123")  # type: ignore[arg-type]


def test_aeroplane_str(fix_init_aeroplane: dict) -> None:
    obj = Aeroplane(**fix_init_aeroplane)
    assert str(obj) == "BOING_001, USA, 200.5, 14444.5"
