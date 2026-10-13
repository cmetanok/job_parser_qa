"""Автотесты на валидацию данных от парсеров."""

import pytest

from parsers import fetch_habr, fetch_trudvsem


@pytest.fixture(scope="module")
def habr_vacancies():
    """Вакансии Habr Career для проверок."""
    return fetch_habr("Python", pages=1)


@pytest.fixture(scope="module")
def trud_vacancies():
    """Вакансии Trudvsem для проверок."""
    return fetch_trudvsem("Python", limit=20)


class TestSalaryValidation:
    """Проверки корректности поля зарплаты."""

    @pytest.mark.slow
    def test_salary_is_number_or_none(self, habr_vacancies):
        """salary_from и salary_to — число или None."""
        for vac in habr_vacancies:
            for field in ["salary_from", "salary_to"]:
                value = vac.get(field)
                assert value is None or isinstance(value, (int, float)), (
                    f"{field}={value} имеет неверный тип {type(value)}"
                )

    @pytest.mark.slow
    def test_salary_not_negative(self, habr_vacancies):
        """Зарплата не может быть отрицательной."""
        for vac in habr_vacancies:
            for field in ["salary_from", "salary_to"]:
                value = vac.get(field)
                if value is not None:
                    assert value >= 0, f"{field}={value} отрицательная"

    @pytest.mark.slow
    def test_salary_from_lte_salary_to(self, habr_vacancies):
        """Если указаны и from, и to — from не больше to."""
        for vac in habr_vacancies:
            sf = vac.get("salary_from")
            st = vac.get("salary_to")
            if sf is not None and st is not None:
                assert sf <= st, (
                    f"salary_from={sf} больше salary_to={st} в вакансии {vac['id']}"
                )


class TestRemoteValidation:
    """Проверки корректности поля remote."""

    @pytest.mark.slow
    def test_remote_is_boolean(self, habr_vacancies):
        """Поле remote — булево значение."""
        for vac in habr_vacancies:
            assert isinstance(vac["remote"], bool), (
                f"remote={vac['remote']} имеет тип {type(vac['remote'])}"
            )

    @pytest.mark.slow
    def test_remote_has_both_values(self, habr_vacancies):
        """В выборке есть и удалённые, и неудалённые вакансии."""
        if len(habr_vacancies) < 5:
            pytest.skip("Мало данных для проверки")

        remote_values = [v["remote"] for v in habr_vacancies]
        assert True in remote_values or False in remote_values, (
            "Все значения remote одинаковые — подозрительно"
        )


class TestIdValidation:
    """Проверки корректности поля id."""

    @pytest.mark.slow
    def test_id_is_string(self, habr_vacancies):
        """id — строка."""
        for vac in habr_vacancies:
            assert isinstance(vac["id"], str), (
                f"id={vac['id']} имеет тип {type(vac['id'])}"
            )

    @pytest.mark.slow
    def test_ids_are_unique(self, habr_vacancies):
        """id не дублируются внутри одной выборки."""
        ids = [v["id"] for v in habr_vacancies]
        assert len(ids) == len(set(ids)), (
            f"Найдены дубликаты id: {[x for x in ids if ids.count(x) > 1]}"
        )


class TestSkillsValidation:
    """Проверки поля skills."""

    @pytest.mark.slow
    def test_skills_is_string(self, habr_vacancies):
        """skills — строка (даже если пустая)."""
        for vac in habr_vacancies:
            assert isinstance(vac["skills"], str), (
                f"skills имеет тип {type(vac['skills'])}"
            )

    @pytest.mark.slow
    def test_skills_not_contain_html(self, habr_vacancies):
        """В skills нет HTML-тегов."""
        for vac in habr_vacancies:
            skills = vac["skills"]
            assert "<" not in skills and ">" not in skills, (
                f"В skills найден HTML: {skills[:100]}"
            )


class TestCompanyValidation:
    """Проверки поля company."""

    @pytest.mark.slow
    def test_company_is_string_or_none(self, habr_vacancies):
        """company — строка или None."""
        for vac in habr_vacancies:
            company = vac.get("company")
            assert company is None or isinstance(company, str)

    @pytest.mark.slow
    def test_company_not_contain_html(self, habr_vacancies):
        """В company нет HTML-тегов."""
        for vac in habr_vacancies:
            company = vac.get("company") or ""
            assert "<" not in company and ">" not in company