# conftest.py
"""Файл conftest.py для хранения фикстур"""

import pytest

from src.airplanes import Aeroplane


@pytest.fixture()
def fix_obj_aeroplane() -> Aeroplane:
    """Возвращает объект класса Aeroplane"""
    return Aeroplane("BORT_007", "Canada", 250.4, 12545.5)


@pytest.fixture()
def fix_init_aeroplane() -> dict:
    """Фикстура входных данных для создания объекта класса"""
    return {
        "callsign": "BOING_001",
        "reg_country": "USA",
        "velocity": 200.5,
        "altitude": 14444.5,
    }


@pytest.fixture()
def fix_list_aeroplanes() -> list[Aeroplane]:
    return [
        Aeroplane("UAE41P", "United Arab Emirates", 73.14, 68.58),
        Aeroplane("GFA2004", "Bahrain", 555.57, 4145.28),
        Aeroplane("FAD437", "Saudi Arabia", 139.49, 1569.72),
    ]
