# views.py
"""Модуль консольного интерфейса."""

from collections.abc import Callable
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Prompt
from rich.table import Table

from src.analytics import filter_aeroplanes_by_keyword, sort_aeroplanes
from src.processing import Processing


def show_aeroplanes(
    aeroplanes: list[dict[str, Any]],
    console: Console,
    title: str,
) -> None:
    """Выводит список самолётов в таблице Rich."""
    if not aeroplanes:
        console.print(
            Panel(
                "[yellow]Самолёты по указанным критериям не найдены.[/yellow]",
                title=title,
                border_style="yellow",
            )
        )
        return

    table = Table(
        title=f"{title}: {len(aeroplanes)}",
        header_style="bold cyan",
        show_lines=True,
    )

    table.add_column("№", justify="right", style="dim", no_wrap=True)
    table.add_column("Позывной", style="bold green")
    table.add_column("Страна регистрации", style="yellow")
    table.add_column("Скорость, м/с", justify="right", style="red")
    table.add_column("Высота, м", justify="right", style="blue")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            description="Формируем таблицу самолётов",
            total=len(aeroplanes),
        )

        for number, plane in enumerate(aeroplanes, start=1):
            table.add_row(
                str(number),
                str(plane.get("callsign", "—")),
                str(plane.get("reg_country", "—")),
                f"{float(plane.get('velocity', 0.0)):.2f}",
                f"{float(plane.get('altitude', 0.0)):.2f}",
            )

            progress.advance(task_id)

    console.print(table)


def filter_and_sort_aeroplanes(
    storage: Processing,
    console: Console,
) -> None:
    """Фильтрует самолёты по ключевому слову и сортирует результат."""
    keyword = Prompt.ask(
        "Введите ключевое слово " "[dim](позывной или страна; Enter — без фильтра)[/dim]",
        default="",
    )

    console.print("\n[bold cyan]Варианты сортировки:[/bold cyan]")
    console.print("1. По позывному: А–Я")
    console.print("2. По высоте: ниже → выше")
    console.print("3. По высоте: выше → ниже")
    console.print("4. По скорости: медленнее → быстрее")
    console.print("5. По скорости: быстрее → медленнее")

    choice = Prompt.ask(
        "Выберите вариант сортировки",
        choices=["1", "2", "3", "4", "5"],
    )

    sort_options = {
        "1": ("callsign", False),
        "2": ("altitude", False),
        "3": ("altitude", True),
        "4": ("velocity", False),
        "5": ("velocity", True),
    }

    sort_by, reverse = sort_options[choice]

    aeroplanes = storage.get_aeroplanes()
    filtered_aeroplanes = filter_aeroplanes_by_keyword(
        aeroplanes,
        keyword,
    )

    sorted_aeroplanes = sort_aeroplanes(
        filtered_aeroplanes,
        sort_by=sort_by,
        reverse=reverse,
    )

    title = "Результат фильтрации и сортировки"

    if keyword.strip():
        title = f"Результат поиска: {keyword.strip()}"

    show_aeroplanes(
        aeroplanes=sorted_aeroplanes,
        console=console,
        title=title,
    )


def user_interaction(
    storage: Processing,
    load_aeroplanes: Callable[[str, Processing], None],
    console: Console,
) -> None:
    """Запускает интерактивное меню приложения."""
    while True:
        console.print("\n[bold cyan]Sky List[/bold cyan]")
        console.print("1. Загрузить самолёты по стране")
        console.print("2. Показать сохранённые самолёты")
        console.print("3. Фильтровать и сортировать самолёты")
        console.print("0. Выйти")

        choice = Prompt.ask(
            "Выберите действие",
            choices=["0", "1", "2", "3"],
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

        if choice == "2":
            show_aeroplanes(
                aeroplanes=storage.get_aeroplanes(),
                console=console,
                title="Сохранённые самолёты",
            )

        if choice == "3":
            filter_and_sort_aeroplanes(storage, console)
