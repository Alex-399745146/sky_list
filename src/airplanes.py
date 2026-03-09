# airplanes.py
"""Модуль классов обработки данных из внешних API"""

from __future__ import annotations

from functools import total_ordering
from typing import Any

from src.abstract import BaseAeroplane
from src.api_clients import APIAdapter


@total_ordering
class Aeroplane(BaseAeroplane):
    """Класс работы с информацией о самолётах."""

    __slots__ = ()  # все слоты уже заданы в BaseAeroplane

    def __init__(
        self,
        callsign: str,
        reg_country: str,
        velocity: float,
        altitude: float,
    ) -> None:
        # Заводим атрибуты в конструктор применяя методы проверки входных данных.
        callsign = self.__validate_callsign(callsign)
        reg_country = self.__validate_reg_country(reg_country)
        velocity = self.__validate_velocity(velocity)
        altitude = self.__validate_altitude(altitude)

        super().__init__(callsign, reg_country, velocity, altitude)

    # ===========> Приватные методы проверок входных данных <===========

    def __validate_callsign(self, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("callsign пустая строка")
        return value.strip()

    def __validate_reg_country(self, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("reg_country пустая строка")
        return value.strip()

    def __validate_velocity(self, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError("velocity должно быть в виде int, float")
        if value < 0:
            raise ValueError("velocity не может быть отрицательной")
        return float(value)

    def __validate_altitude(self, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError("altitude должна быть int, float")
        if value < 0:
            raise ValueError("altitude не может быть отрицательной")
        return float(value)

    # ===========> Шесть методов сравнения через functools <===========

    # functools по аналогии достроит другие 4 варианта сравнений (<=, >, >=, !=)
    def __eq__(self, other: object) -> bool:
        """Метод сравнения == равно, обязательный метод для functools"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        # считаем самолёты равными, если совпадает скорость и высота
        return self.velocity == other.velocity and self.altitude == other.altitude

    def __lt__(self, other: object) -> bool:
        """Метод сравнения < меньше для построения functools"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        # сначала сравниваем по высоте, при равной высоте — по скорости
        if self.altitude == other.altitude:
            return self.velocity < other.velocity
        return self.altitude < other.altitude

    # ===========> Обработка данных от внешнего API <===========

    @classmethod
    def get_filter_aeroplanes(cls, aeroplanes: dict[str, Any]) -> list["Aeroplane"]:
        """
        Преобразует сырые данные из opensky (ключ 'states')
        в список объектов Aeroplane.
        """
        states = aeroplanes.get("states") or []
        result: list[Aeroplane] = []

        for state in states:
            callsign = state[1] or ""
            reg_country = state[2] or ""
            altitude = state[7] or 0.0
            velocity = state[9] or 0.0

            try:
                plane = cls(
                    callsign=callsign,
                    reg_country=reg_country,
                    velocity=velocity,
                    altitude=altitude,
                )
            except (TypeError, ValueError):
                # некорректные данные пропускаем
                continue

            result.append(plane)

        return result


if __name__ == "__main__":
    api = APIAdapter()
    api.get_aeroplanes("Canada")

    if api.aeroplanes is None:
        print("Данных о самолётах нет")
    else:
        planes = Aeroplane.get_filter_aeroplanes(api.aeroplanes)

        p1, p2 = planes[0], planes[1]
        print(p1.callsign, p1.velocity, p1.altitude)
        print(p2.callsign, p2.velocity, p2.altitude)

        print(p1 > p2)  # сравнение по высоте, затем по скорости
