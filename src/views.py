# views.py
"""Модуль консольного интерфейса."""

from collections.abc import Callable
from typing import Iterable

from rich.console import Console
from rich.prompt import Prompt

from src.airplanes import Aeroplane
from src.api_clients import APIAdapter
from src.processing import Processing


def load_aeroplanes_by_country(country: str) -> list[Aeroplane]:
    """Загружает и преобразует данные о самолётах для указанной страны."""
    api = APIAdapter()
    api.get_aeroplanes(country)

    if api.aeroplanes is None:
        print("Данных о самолётах нет")
        return []

    # Преобразование массива данных в список объектов Aeroplane
    planes = Aeroplane.get_filter_aeroplanes(api.aeroplanes)

    # Сохраняем все самолёты в JSON
    storage = Processing()
    for plane in planes:

        storage.add_aeroplane(
            {
                "callsign": plane.callsign,
                "reg_country": plane.reg_country,
                "velocity": plane.velocity,
                "altitude": plane.altitude,
            }
        )

    return planes


def filter_aeroplanes(aeroplanes: Iterable[Aeroplane], reg_countries: list[str]) -> list[Aeroplane]:
    """Фильтрация самолётов по стране регистрации (origin_country)"""
    if not reg_countries:
        return list(aeroplanes)

    reg_countries_norm = {c.strip().lower() for c in reg_countries if c.strip()}
    return [plane for plane in aeroplanes if plane.reg_country.lower() in reg_countries_norm]


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


def get_aeroplanes_by_altitude(aeroplanes: Iterable[Aeroplane], altitude_range: str) -> list[Aeroplane]:
    """Фильтрация самолётов по диапазону высот."""
    low, high = parse_altitude_range(altitude_range)
    return [plane for plane in aeroplanes if low <= plane.altitude <= high]


def sort_aeroplanes(aeroplanes: Iterable[Aeroplane]) -> list[Aeroplane]:
    """
    Сортировка самолётов, поскольку в Aeroplane реализованы __lt__/__eq__...,
    sorted() может использовать их напрямую.
    """
    return sorted(aeroplanes, reverse=True)  # от большего к меньшему (высота, потом скорость)


def get_top_aeroplanes(aeroplanes: Iterable[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Возвращает топ N самолётов из уже отсортированного списка."""
    return list(aeroplanes)[:top_n]


def print_aeroplanes(aeroplanes: Iterable[Aeroplane]) -> None:  # pragma: no cover
    """Функция вывода заглавия данных в таблице"""
    header = f"{'ID борта':<15}" f"{'Страна регистрации':<28}" f"{'Скорость (м/с)':>15}" f"{'Высота (м)':>15}"
    print(header)
    print("-" * len(header))

    for plane in aeroplanes:
        print(f"{plane.callsign:<15}" f"{plane.reg_country:<28}" f"{plane.velocity:15.2f}" f"{plane.altitude:15.2f}")


def user_interaction(
    storage: Processing,
    load_aeroplanes: Callable[[str, Processing], None],
    console: Console,
) -> None:
    """Запускает интерактивное меню приложения."""

    while True:
        console.print("\n[bold cyan]Sky List[/bold cyan]")
        console.print("1. Загрузить самолёты по стране")
        console.print("0. Выйти")

        choice = Prompt.ask(
            "Выберите действие",
            choices=["0", "1"],
        )

        if choice == "0":
            console.print("[green]Работа программы завершена.[/green]")
            break

        if choice == "1":
            country = Prompt.ask("Введите страну").strip()

            if not country:
                console.print("[red]Название страны не должно быть пустым.[/red]")
                continue

            load_aeroplanes(country, storage)
