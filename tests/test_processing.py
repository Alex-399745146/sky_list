# test_processing.py
"""Тест кейсы проверки обработки информации class Processing"""

from src.processing import Processing


def test_get_aeroplanes_filters_by_country(tmp_path):
    # Используем временный файл
    file_path = tmp_path / "planes.json"
    storage = Processing()
    storage._file_path = file_path  # переназначаем атрибут - путь к файлу только в тесте

    storage.add_aeroplane({"callsign": "BOING_001", "reg_country": "Canada", "velocity": 200.5, "altitude": 14444.5})
    storage.add_aeroplane({"callsign": "BOING_002", "reg_country": "Russia", "velocity": 210.0, "altitude": 12000.0})

    result = storage.get_aeroplanes(reg_country="Canada")

    assert isinstance(result, list)
    assert len(result) == 1
    plane = result[0]
    assert plane["callsign"] == "BOING_001"
    assert plane["reg_country"] == "Canada"


def test_get_aeroplanes_filters_by_altitude(tmp_path):
    file_path = tmp_path / "planes.json"
    storage = Processing()
    storage._file_path = file_path

    storage.add_aeroplane({"callsign": "LOW", "reg_country": "Iran", "velocity": 180.0, "altitude": 9000.0})
    storage.add_aeroplane({"callsign": "MID", "reg_country": "Iran", "velocity": 190.0, "altitude": 12000.0})
    storage.add_aeroplane({"callsign": "HIGH", "reg_country": "Iran", "velocity": 200.0, "altitude": 16000.0})

    result = storage.get_aeroplanes(reg_country="Iran", min_altitude=10000, max_altitude=15000)

    assert len(result) == 1
    assert result[0]["callsign"] == "MID"


def test_delete_aeroplanes_by_country(tmp_path):
    file_path = tmp_path / "planes.json"
    storage = Processing()
    storage._file_path = file_path

    storage.add_aeroplane({"callsign": "CA1", "reg_country": "Canada", "velocity": 200.5, "altitude": 11000.0})
    storage.add_aeroplane({"callsign": "RU1", "reg_country": "Russia", "velocity": 210.0, "altitude": 12000.0})

    storage.delete_aeroplanes(reg_country="Canada")

    remaining = storage.get_aeroplanes()
    assert len(remaining) == 1
    assert remaining[0]["reg_country"] == "Russia"


def test_clear_storage(tmp_path) -> None:
    """Проверка очистки данных локального хранилища."""
    storage = Processing()
    storage._file_path = tmp_path / "aeroplanes.json"

    storage.add_aeroplane(
        {
            "callsign": "UAE41P",
            "reg_country": "United Arab Emirates",
            "velocity": 73.14,
            "altitude": 68.58,
        }
    )

    assert len(storage.get_aeroplanes()) == 1

    storage.clear_storage()

    assert storage.get_aeroplanes() == []


def test_add_aeroplanes_adds_multiple_unique_records(tmp_path) -> None:
    """Проверка пакетного добавления самолётов без дубликатов."""
    storage = Processing()
    storage._file_path = tmp_path / "aeroplanes.json"

    added_count = storage.add_aeroplanes(
        [
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
                "callsign": "UAE41P",
                "reg_country": "United Arab Emirates",
                "velocity": 100.0,
                "altitude": 1000.0,
            },
        ]
    )

    result = storage.get_aeroplanes()

    assert added_count == 2
    assert len(result) == 2
    assert {item["callsign"] for item in result} == {"UAE41P", "GFA2004"}


def test_get_all_aeroplanes(tmp_path) -> None:
    """Проверка получения всех сохранённых самолётов."""
    storage = Processing()
    storage._file_path = tmp_path / "aeroplanes.json"

    storage.add_aeroplanes(
        [
            {
                "callsign": "UAE41P",
                "reg_country": "United Arab Emirates",
                "velocity": 73.14,
                "altitude": 68.58,
            },
            {
                "callsign": "FAD437",
                "reg_country": "Saudi Arabia",
                "velocity": 139.49,
                "altitude": 1569.72,
            },
        ]
    )

    result = storage.get_aeroplanes()

    assert len(result) == 2
    assert result[0]["callsign"] == "UAE41P"
    assert result[1]["callsign"] == "FAD437"
