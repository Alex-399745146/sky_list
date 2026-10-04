# main.py
"""Модуль основной логики"""

import logging

from src.views import user_interaction

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

if __name__ == "__main__":  # pragma: no cover
    user_interaction()
