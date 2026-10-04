# api_clients.py
"""Модуль с классами для работы по внешним API"""

import logging
from json import JSONDecodeError
from typing import Any, Dict, Union

from requests import RequestException, Response, get

from src.abstract import BaseApi

logger = logging.getLogger(__name__)


ParamsValue = Union[str, int, float]


class APIAdapter(BaseApi):
    """Дочерний класс работы с внешними сервисами по API"""

    __url_map: str  # nominatim.openstreetmap.org
    __url_sky: str  # opensky-network.org
    __aeroplanes: Any | None
    __error_message: str | None

    def __init__(self) -> None:
        super().__init__()  # Два атрибута базового класса.
        self.__aeroplanes = None  # Добавим атрибут для использования.
        self.__error_message = None

    @property
    def aeroplanes(self) -> Any | None:
        """Метод обращения к уже имеющимся данным для их чтения"""
        return self.__aeroplanes

    def get_aeroplanes(self, country: str) -> None:
        """Получает данные о самолётах по стране."""
        self.__aeroplanes = None
        self.__error_message = None

        headers_nominatim: Dict[str, str] = {
            "User-Agent": "test-app/1.0",
        }

        params_nominatim: Dict[str, ParamsValue] = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response_map: Response = get(
                url=self.url_map,
                params=params_nominatim,
                headers=headers_nominatim,
                timeout=10,
            )
        except RequestException as error:
            message = f"Не удалось получить координаты страны {country!r}: {error}"

            logger.error(message)

            self.__aeroplanes = None
            self.__error_message = message
            return

        if response_map.status_code != 200:
            message = "Nominatim вернул некорректный HTTP-статус: " f"{response_map.status_code}"

            logger.error(message)

            self.__aeroplanes = None
            self.__error_message = message
            return

        try:
            data_map = response_map.json()
        except JSONDecodeError as error:
            message = f"Nominatim вернул некорректный JSON: {error}"

            logger.error(message)

            self.__error_message = message
            return

        if not data_map:
            logger.warning(
                "От nominatim.openstreetmap.org пришёл пустой список стран (country=%r)",
                country,
            )
            self.__aeroplanes = None
            return

        geo_coordinates = data_map[0].get("boundingbox")

        if not geo_coordinates or len(geo_coordinates) < 4:
            logger.warning(
                "Не удалось получить корректные координаты страны (country=%r, data=%r)",
                country,
                data_map,
            )
            self.__aeroplanes = None
            return

        try:
            params: Dict[str, float] = {
                "lamin": float(geo_coordinates[0]),
                "lamax": float(geo_coordinates[1]),
                "lomin": float(geo_coordinates[2]),
                "lomax": float(geo_coordinates[3]),
            }
        except (TypeError, ValueError) as error:
            message = f"Nominatim вернул некорректные координаты: {error}"

            logger.error(message)

            self.__error_message = message
            return

        try:
            response_sky: Response = get(
                url=self.url_sky,
                params=params,
                timeout=10,
            )
        except RequestException as error:
            message = f"Не удалось получить данные OpenSky: {error}"

            logger.error(message)

            self.__aeroplanes = None
            self.__error_message = message
            return

        if response_sky.status_code != 200:
            message = "OpenSky вернул некорректный HTTP-статус: " f"{response_sky.status_code}"

            logger.error(message)

            self.__aeroplanes = None
            self.__error_message = message
            return

        try:
            self.__aeroplanes = response_sky.json()
        except JSONDecodeError as error:
            message = f"OpenSky вернул некорректный JSON: {error}"

            logger.error(message)

            self.__error_message = message

    @property
    def error_message(self) -> str | None:
        """Возвращает последнее сообщение об ошибке API."""
        return self.__error_message


if __name__ == "__main__":  # pragma: no cover
    api = APIAdapter()
    api.get_aeroplanes("Iran")
    data = api.aeroplanes
    print(type(data))
    print(data)
    if data is None:
        print("Данных о самолётах нет")
    else:
        # api.aeroplanes — dict (ответ JSON от opensky)
        for inf_plane in data["states"]:
            print(inf_plane)
