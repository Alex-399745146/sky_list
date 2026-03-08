# api_clients.py
"""Модуль с классами для работы по внешним API"""

from typing import Any
from requests import get, Response

from src.abstract import BaseApi


class APIAdapter(BaseApi):
    """Дочерний класс работы с внешними сервисами по API"""
    __url_map: str  # nominatim.openstreetmap.org
    __url_sky: str  # opensky-network.org
    __aeroplanes: Any | None

    def __init__(self) -> None:
        super().__init__()  #  Два атрибута базового класса.
        self.__aeroplanes = None  # Добавим атрибут для использования.

    @property
    def aeroplanes(self) -> Any | None:
        """Метод обращения к данным для их чтения"""
        return self.__aeroplanes

    def get_aeroplanes(self, country: str) -> None:
        """Метод выдачи данных о самолётах"""
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        response_map: Response = get(
            url=self.url_map,
            params=params_nominatim,
            headers=headers_nominatim,
            timeout=10,
        )

        if response_map.status_code != 200:
            print(
                f"От nominatim.openstreetmap.org получен некорректный ответ: "
                f"{response_map.status_code}"
            )
            self.__aeroplanes = None
            return

        data_map = response_map.json()

        if not data_map:
            print("От nominatim.openstreetmap.org пришёл пустой список стран")
            self.__aeroplanes = None
            return

        geo_coordinates = data_map[0].get('boundingbox')

        if not geo_coordinates or len(geo_coordinates) < 4:
            print("Не удалось получить корректные координаты страны")
            self.__aeroplanes = None
            return

        params = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }

        response_sky: Response = get(
            url=self.url_sky,
            params=params,
            timeout=10,
        )

        if response_sky.status_code != 200:
            print(
                f"От opensky-network.org получен некорректный ответ: "
                f"{response_sky.status_code}"
            )
            self.__aeroplanes = None
            return

        data_sky: Any = response_sky.json()
        self.__aeroplanes = data_sky


if __name__ == '__main__':
    api = APIAdapter()
    api.get_aeroplanes('Iran')

    if api.aeroplanes is None:
        print("Данных о самолётах нет")
    else:
        # api.aeroplanes — dict (ответ JSON от opensky)
        for inf_plane in api.aeroplanes["states"]:
            print(inf_plane)
