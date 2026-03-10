# processing.py
"""Модуль классов операционистов"""

import json
from typing import Any

from src.abstract import BaseProcessing


class Processing(BaseProcessing):
    """Класс для сохранения информации о самолётах в JSON-файл."""

    def _read_all(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        if not isinstance(data, list):
            return []
        return data

    def _write_all(self, data: list[dict[str, Any]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane_data: dict[str, Any]) -> None:
        """Добавить запись о самолёте в JSON-файл, избегая дублей."""
        data = self._read_all()

        callsign = aeroplane_data.get("callsign")
        reg_country = aeroplane_data.get("reg_country")

        # Проверяем если уже в файле такой самолет, чтоб не дублировать
        for item in data:
            if item.get("callsign") == callsign and item.get("reg_country") == reg_country:
                return

        data.append(aeroplane_data)
        self._write_all(data)

    def get_aeroplanes(self, **criteria: Any) -> list[dict[str, Any]]:
        """
        Фильтрация записей по введённым критериям.
        Например: reg_country="Iran", min_altitude=10000, max_altitude=15000
        """
        data = self._read_all()

        reg_country = criteria.get("reg_country")
        min_altitude = criteria.get("min_altitude")
        max_altitude = criteria.get("max_altitude")

        result: list[dict[str, Any]] = []

        for item in data:
            ok = True

            if reg_country is not None:
                if str(item.get("reg_country", "")).lower() != str(reg_country).lower():
                    ok = False

            altitude = item.get("altitude")
            if min_altitude is not None and altitude is not None:
                if altitude < min_altitude:
                    ok = False
            if max_altitude is not None and altitude is not None:
                if altitude > max_altitude:
                    ok = False

            if ok:
                result.append(item)

        return result

    def delete_aeroplanes(self, **criteria: Any) -> None:
        """Удалить записи, которые удовлетворяют критериям."""
        data = self._read_all()
        to_keep: list[dict[str, Any]] = []

        reg_country = criteria.get("reg_country")
        min_altitude = criteria.get("min_altitude")
        max_altitude = criteria.get("max_altitude")

        for item in data:
            remove = False

            if reg_country is not None:
                if str(item.get("reg_country", "")).lower() == str(reg_country).lower():
                    remove = True

            altitude = item.get("altitude")
            if min_altitude is not None and altitude is not None:
                if altitude >= min_altitude:
                    remove = True
            if max_altitude is not None and altitude is not None:
                if altitude <= max_altitude:
                    remove = True

            if not remove:
                to_keep.append(item)

        self._write_all(to_keep)


if __name__ == "__main__":  # pragma: no cover
    from src.airplanes import Aeroplane

    storage = Processing()

    plane = Aeroplane("UAL1621", "Canada", 268.79, 10203.18)

    storage.add_aeroplane(
        {
            "callsign": plane.callsign,
            "reg_country": plane.reg_country,
            "velocity": plane.velocity,
            "altitude": plane.altitude,
        }
    )

    canada_planes = storage.get_aeroplanes(reg_country="Canada")
    # print("Самолёты, зарегистрированные в Canada:", canada_planes)

    storage.delete_aeroplanes(reg_country="USA")
    print("Самолёты, зарегистрированные в Canada:", canada_planes)
