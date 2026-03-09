# abstract.py
"""Модуль с абстрактными классами"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseApi(ABC):
    """Абстрактный базовый класс для APIAdapter"""

    __url_map: str
    __url_sky: str

    def __init__(self) -> None:
        self.__url_map: str = "https://nominatim.openstreetmap.org/search"
        self.__url_sky: str = "https://opensky-network.org/api/states/all?"

    @property
    def url_map(self) -> str:
        return self.__url_map

    @property
    def url_sky(self) -> str:
        return self.__url_sky

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """Абстрактный метод загрузки данных по самолётам"""
        raise NotImplementedError("Метод get_aeroplanes ещё не определен")


class BaseAeroplane(ABC):
    """Абстрактный базовый класс для обработки данных о самолётах"""

    #  Для ограничения набора атрибутов и экономии памяти.
    __slots__ = ("_callsign", "_reg_country", "_velocity", "_altitude")

    def __init__(self, callsign: str, reg_country: str, velocity: float, altitude: float) -> None:
        self._callsign = callsign
        self._reg_country = reg_country
        self._velocity = velocity
        self._altitude = altitude

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def reg_country(self) -> str:
        return self._reg_country

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def altitude(self) -> float:
        return self._altitude

    @classmethod
    @abstractmethod
    def get_filter_aeroplanes(cls, aeroplanes: dict[str, Any]) -> list[Any]:
        """Абстрактный метод обработки данных о самолётах"""
        raise NotImplementedError("Метод get_filter_aeroplanes ещё не определен")


class BaseProcessing(ABC):
    """Абстрактный класс для работы с файлами и данными о самолётах"""

    __filename: str  # Имя файла сохраняющего данные.

    def __init__(self, __filename: str = "aeroplanes.json") -> None:
        root_dir = Path(__file__).resolve().parent.parent  # src -> корень проекта
        data_dir = root_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)  # создаём, если нет

        self._file_path = data_dir / __filename

    @property
    def file_path(self) -> Path:
        return self._file_path

    @abstractmethod
    def add_aeroplane(self, aeroplane_data: dict[str, Any]) -> None:
        """Добавить информацию о самолёте в файл"""
        raise NotImplementedError

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> list[dict[str, Any]]:
        """
        Получить данные из файла по указанным критериям.
        Пример критериев: reg_country="Iran", min_altitude=10000, max_altitude=15000.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_aeroplanes(self, **criteria: Any) -> None:
        """Удалить информацию о самолётах в файле по указанным критериям"""
        raise NotImplementedError
