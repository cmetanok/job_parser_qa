"""Автотесты для парсеров Habr Career и Trudvsem."""

import pytest

from parsers import fetch_habr, fetch_trudvsem


# --- Habr Career ---

class TestHabrParser:
    """Тесты парсера Habr Career."""

    @pytest.mark.smoke
    @pytest.mark.slow
    def test_fetch_returns_list(self):
        """Парсер возвращает список."""
        result = fetch_habr("Python", pages=1)
        assert isinstance(result, list)

    @pytest.mark.smoke
    @pytest.mark.slow
    def test_fetch_returns_vacancies(self):
        """По популярному запросу возвращается хотя бы одна вакансия."""
        result = fetch_habr("Python", pages=1)
        assert len(result) > 0, "Habr Career вернул пустой список для 'Python'"

    @pytest.mark.smoke
    @pytest.mark.slow
    def test_vacancy_has_required_fields(self):
        """Каждая вакансия содержит обязательные поля."""
        result = fetch_habr("Python", pages=1)
        required = ["source", "id", "name", "url", "remote"]
        for vac in result:
            for field in required:
                assert field in vac, f"Поле '{field}' отсутствует в вакансии"

    @pytest.mark.smoke
    @pytest.mark.slow
    def test_source_field_is_correct(self):
        """Поле source содержит 'Habr Career'."""
        result = fetch_habr("Python", pages=1)
        for vac in result:
            assert vac["source"] == "Habr Career"

    @pytest.mark.slow
    def test_url_starts_with_https(self):
        """URL вакансии начинается с https://."""
        result = fetch_habr("Python", pages=1)
        for vac in result:
            assert vac["url"].startswith("https://")

    @pytest.mark.slow
    def test_name_is_not_empty(self):
        """Название вакансии не пустое."""
        result = fetch_habr("Python", pages=1)
        for vac in result:
            assert vac["name"]
            assert len(vac["name"].strip()) > 0

    @pytest.mark.slow
    @pytest.mark.negative
    def test_empty_query_returns_list(self):
        """Пустой запрос не ломает парсер."""
        result = fetch_habr("", pages=1)
        assert isinstance(result, list)

    @pytest.mark.slow
    @pytest.mark.negative
    def test_nonexistent_query_returns_empty_or_list(self):
        """Несуществующий запрос возвращает пустой список или список без ошибок."""
        result = fetch_habr("asdfghjklqwerty123", pages=1)
        assert isinstance(result, list)


# --- Trudvsem ---

class TestTrudvsemParser:
    """Тесты парсера Trudvsem."""

    @pytest.mark.smoke
    @pytest.mark.slow
    def test_fetch_returns_list(self):
        """Парсер возвращает список."""
        result = fetch_trudvsem("Python", limit=10)
        assert isinstance(result, list)

    @pytest.mark.smoke
    @pytest.mark.slow
    def test_vacancy_has_required_fields(self):
        """Каждая вакансия содержит обязательные поля."""
        result = fetch_trudvsem("Python", limit=10)
        if not result:
            pytest.skip("Trudvsem вернул пустой список, нет данных для проверки")
        required = ["source", "id", "name", "url", "remote"]
        for vac in result:
            for field in required:
                assert field in vac, f"Поле '{field}' отсутствует"

    @pytest.mark.slow
    def test_source_field_is_correct(self):
        """Поле source содержит 'Trudvsem'."""
        result = fetch_trudvsem("Python", limit=10)
        for vac in result:
            assert vac["source"] == "Trudvsem"

    @pytest.mark.slow
    def test_url_starts_with_https(self):
        """URL вакансии начинается с https://."""
        result = fetch_trudvsem("Python", limit=10)
        for vac in result:
            if vac.get("url"):
                assert vac["url"].startswith("https://")

    @pytest.mark.slow
    @pytest.mark.negative
    def test_empty_query_returns_list(self):
        """Пустой запрос не ломает парсер."""
        result = fetch_trudvsem("", limit=10)
        assert isinstance(result, list)


# --- Сравнение источников ---

class TestSourceComparison:
    """Проверки, общие для обоих источников."""

    @pytest.mark.slow
    def test_both_parsers_return_same_structure(self):
        """Оба парсера возвращают словари с одинаковым набором полей."""
        habr = fetch_habr("Python", pages=1)
        trud = fetch_trudvsem("Python", limit=10)

        if not habr or not trud:
            pytest.skip("Нет данных от одного из источников")

        habr_keys = set(habr[0].keys())
        trud_keys = set(trud[0].keys())

        assert habr_keys == trud_keys, (
            f"Структура данных отличается.\n"
            f"Только в Habr: {habr_keys - trud_keys}\n"
            f"Только в Trudvsem: {trud_keys - habr_keys}"
        )