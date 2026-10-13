"""Настройка pytest: пути к парсерам основного проекта."""

import sys
from pathlib import Path

import pytest

# Точный путь к локальной копии проекта vacancy-dashboard.
PROJECT_PATH = Path(r"C:\Users\ilyap\PycharmProjects\vacancy-dashboard")

if not PROJECT_PATH.exists():
    pytest.exit(
        f"Не найден проект по пути: {PROJECT_PATH}\n"
        f"Проверь путь или измени переменную PROJECT_PATH в conftest.py"
    )

# Добавляем корень проекта в sys.path, чтобы `from parsers import ...` работал
sys.path.insert(0, str(PROJECT_PATH))