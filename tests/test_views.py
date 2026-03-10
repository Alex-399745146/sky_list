# test_processing.py
"""Тест функций модуля views"""

from src.airplanes import Aeroplane
from src.views import (filter_aeroplanes, get_aeroplanes_by_altitude, get_top_aeroplanes, load_aeroplanes_by_country,
                       sort_aeroplanes)


def test_load_aeroplanes_by_country():
    result = load_aeroplanes_by_country("")

    assert isinstance(result, list)
    assert len(result) == 0


def test_filter_aeroplanes(fix_list_aeroplanes):
    result = filter_aeroplanes(fix_list_aeroplanes, ["Saudi Arabia"])

    assert isinstance(result, list)
    assert len(result) == 1

    plane = result[0]

    assert isinstance(plane, Aeroplane)
    assert plane.reg_country == "Saudi Arabia"
    assert plane.callsign == "FAD437"


def test_get_aeroplanes_by_altitude(fix_list_aeroplanes):
    result = get_aeroplanes_by_altitude(fix_list_aeroplanes, "")

    assert isinstance(result, list)
    assert len(result) == 3


def test_sort_aeroplanes(fix_list_aeroplanes):
    result = sort_aeroplanes(fix_list_aeroplanes)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0].reg_country == "Bahrain"


def test_get_top_aeroplanes(fix_list_aeroplanes):
    result = get_top_aeroplanes(fix_list_aeroplanes, 2)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].reg_country == "United Arab Emirates"
