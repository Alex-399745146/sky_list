# src/analytics.py
"""Функции фильтрации и сортировки данных о самолётах."""

from typing import Any


def filter_aeroplanes_by_keyword(
    aeroplanes: list[dict[str, Any]],
    keyword: str,
) -> list[dict[str, Any]]:
    """Фильтрует самолёты по позывному или стране регистрации."""
    normalized_keyword = keyword.strip().casefold()

    if not normalized_keyword:
        return aeroplanes.copy()

    return [
        plane
        for plane in aeroplanes
        if normalized_keyword in str(plane.get("callsign", "")).casefold()
        or normalized_keyword in str(plane.get("reg_country", "")).casefold()
    ]


def sort_aeroplanes(
    aeroplanes: list[dict[str, Any]],
    sort_by: str,
    reverse: bool = False,
) -> list[dict[str, Any]]:
    """Сортирует самолёты по указанному полю."""

    allowed_fields = {
        "callsign",
        "velocity",
        "altitude",
    }

    if sort_by not in allowed_fields:
        raise ValueError(f"Неподдерживаемое поле сортировки: {sort_by}")

    if sort_by == "callsign":
        return sorted(
            aeroplanes,
            key=lambda plane: str(plane.get("callsign", "")).casefold(),
            reverse=reverse,
        )

    return sorted(
        aeroplanes,
        key=lambda plane: float(plane.get(sort_by, 0.0)),
        reverse=reverse,
    )
