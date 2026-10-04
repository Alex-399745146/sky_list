# main.py
"""Точка входа и основная логика консольного приложения."""

import logging

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from src.airplanes import Aeroplane
from src.api_clients import APIAdapter
from src.processing import Processing
from src.views import user_interaction

console = Console()


def configure_logging() -> None:
    """Настраивает логирование приложения."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def load_aeroplanes(country: str, storage: Processing) -> None:
    """Загружает, нормализует и сохраняет самолёты указанной страны."""

    api = APIAdapter()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            description=f"Получаем данные по стране: {country}",
            total=None,
        )

        api.get_aeroplanes(country)

        raw_data = api.aeroplanes or {}

        progress.update(
            task_id,
            description="Нормализуем данные самолётов",
        )

        aeroplanes = Aeroplane.get_filter_aeroplanes(raw_data)

        progress.update(
            task_id,
            description="Сохраняем данные в хранилище",
        )

        for plane in aeroplanes:
            storage.add_aeroplane(
                {
                    "callsign": plane.callsign,
                    "reg_country": plane.reg_country,
                    "velocity": plane.velocity,
                    "altitude": plane.altitude,
                }
            )

    if not aeroplanes:
        console.print(
            Panel(
                f"[yellow]По стране {country!r} валидные данные не найдены.[/yellow]",
                title="Результат загрузки",
                border_style="yellow",
            )
        )
        return

    console.print(
        Panel(
            f"[bold green]Успешно сохранено самолётов: {len(aeroplanes)}[/bold green]",
            title="Загрузка завершена",
            border_style="green",
        )
    )


def main() -> None:
    """Запускает приложение."""
    configure_logging()

    storage = Processing()
    storage.clear_storage()

    console.print(
        Panel(
            "[bold cyan]Sky List[/bold cyan]\n"
            "Данные текущего сеанса будут сохранены только до завершения программы.",
            title="Добро пожаловать",
            border_style="cyan",
        )
    )

    user_interaction(storage, load_aeroplanes, console)


if __name__ == "__main__":  # pragma: no cover
    main()
