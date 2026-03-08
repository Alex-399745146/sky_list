# main.py
"""Модуль основной логики"""

from typing import Iterable

from src.api_clients import APIAdapter
from src.airplanes import Aeroplane


def load_aeroplanes_by_country(country: str) -> list[Aeroplane]:
    """Загружает и преобразует данные о самолётах для указанной страны."""
    api = APIAdapter()
    api.get_aeroplanes(country)

    if api.aeroplanes is None:
        print("Данных о самолётах нет")
        return []

    # Преобразование набора данных в список объектов Aeroplane
    return Aeroplane.get_filter_aeroplanes(api.aeroplanes)


def filter_aeroplanes(
    aeroplanes: Iterable[Aeroplane],
    reg_countries: list[str],
) -> list[Aeroplane]:
    """Фильтрация самолётов по стране регистрации (origin_country)."""
    if not reg_countries:
        return list(aeroplanes)

    reg_countries_norm = {c.strip().lower() for c in reg_countries if c.strip()}
    return [
        plane
        for plane in aeroplanes
        if plane.reg_country.lower() in reg_countries_norm
    ]


def parse_altitude_range(raw: str) -> tuple[float, float]:
    """Парсит строку диапазона высот вида '1000-2000' или '1000 - 2000'."""
    raw = raw.strip()
    if not raw:
        # Пустая строка — без ограничений по высоте
        return float("-inf"), float("inf")

    parts = raw.replace(" ", "").split("-")
    if len(parts) != 2:
        raise ValueError("Диапазон высот должен быть в формате: min-max")

    low, high = map(float, parts)
    if low > high:
        low, high = high, low
    return low, high


def get_aeroplanes_by_altitude(
    aeroplanes: Iterable[Aeroplane],
    altitude_range: str,
) -> list[Aeroplane]:
    """Фильтрация самолётов по диапазону высот."""
    low, high = parse_altitude_range(altitude_range)
    return [plane for plane in aeroplanes if low <= plane.altitude <= high]


def sort_aeroplanes(aeroplanes: Iterable[Aeroplane]) -> list[Aeroplane]:
    """
    Сортировка самолётов.
    Поскольку в Aeroplane реализованы __lt__/__eq__,
    sorted() может использовать их напрямую.
    """
    return sorted(aeroplanes, reverse=True)  # от большего к меньшему (высота, потом скорость)


def get_top_aeroplanes(
    aeroplanes: Iterable[Aeroplane],
    top_n: int,
) -> list[Aeroplane]:
    """Возвращает топ N самолётов из уже отсортированного списка."""
    return list(aeroplanes)[:top_n]


def print_aeroplanes(aeroplanes: Iterable[Aeroplane]) -> None:
    header = (
        f"{'Callsign':<15}"
        f"{'Country':<25}"
        f"{'Velocity':>12}"
        f"{'Altitude':>12}"
    )
    print(header)
    print("-" * len(header))

    for plane in aeroplanes:
        print(
            f"{plane.callsign:<15}"
            f"{plane.reg_country:<25}"
            f"{plane.velocity:12.2f}"
            f"{plane.altitude:12.2f}"
        )


def user_interaction() -> None:
    """Функция взаимодействия с пользователем."""
    country = input("Введите название страны для запроса к API: ").strip()
    top_n = int(input("Введите количество самолётов для вывода в топ N: ").strip())
    filter_words = input(
        "Введите названия стран регистрации (через пробел) для фильтрации: "
    ).split()
    altitude_range = input(
        "Введите диапазон высот полёта (например: 1000-15000): "
    ).strip()

    # 1. Загружаем самолёты по стране
    aeroplanes = load_aeroplanes_by_country(country)
    if not aeroplanes:
        return

    # 2. Фильтрация по стране регистрации
    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    # 3. Фильтрация по диапазону высот
    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)

    # 4. Сортировка и выбор топ N
    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

    # 5. Вывод
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()
