# test_abstract.py
"""Модуль с кейсами проверок базовых абстрактных классов"""

import pytest

from src.abstract import BaseAeroplane, BaseApi, BaseProcessing


def test_base_api_is_abstract() -> None:
    """Нельзя создавать экземпляр BaseApi."""
    with pytest.raises(TypeError) as exc_info:
        BaseApi()  # type: ignore[abstract]

    msg = str(exc_info.value)
    assert "abstract" in msg
    assert "BaseApi" in msg


def test_base_aeroplane_is_abstract() -> None:
    """Нельзя создавать экземпляр BaseAeroplane."""
    with pytest.raises(TypeError) as exc_info:
        BaseAeroplane("CALL", "Country", 100.0, 1000.0)  # type: ignore[abstract]

    msg = str(exc_info.value)
    assert "abstract" in msg
    assert "BaseAeroplane" in msg


def test_base_processing_is_abstract() -> None:
    """Нельзя создавать экземпляр BaseProcessing."""
    with pytest.raises(TypeError) as exc_info:
        BaseProcessing()  # type: ignore[abstract]

    msg = str(exc_info.value)
    assert "abstract" in msg
    assert "BaseProcessing" in msg
