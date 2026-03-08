# abstract.py
"""Модуль с абстрактными классами"""

from abc import ABC, abstractmethod


class BaseApi(ABC):
    """Абстрактный базовый класс для APIAdapter"""
    __url_map: str
    __url_sky: str

    def __init__(self) -> None:
        self.__url_map = "https://nominatim.openstreetmap.org/search"
        self.__url_sky = "https://opensky-network.org/api/states/all?"

    @property
    def url_map(self) -> str:
        return self.__url_map

    @property
    def url_sky(self) -> str:
        return self.__url_sky

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """Абстрактный метод загрузки данных по самолётам"""
        raise NotImplementedError("Метод ещё не определен")
