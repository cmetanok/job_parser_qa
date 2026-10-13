# Автотесты для Job Parser

Набор автотестов на pytest для проверки парсеров и валидации данных проекта [Job Parser](https://github.com/cmetanok/job_parser).

## Что проверяется

| Файл | Что тестирует |
|------|---------------|
| `test_parsers.py` | Структура данных, возвращаемых парсерами Habr Career и Trudvsem |
| `test_data_validation.py` | Типы полей, диапазоны, edge-кейсы, отсутствие HTML в тексте |

## Итоги прогона

```
25 passed in 188.99s (0:03:08)
```

Все 25 тестов проходят успешно.

## Установка

```bash
cd autotests
pip install -r requirements.txt
```

## Подготовка

Тесты импортируют парсеры из локальной копии основного проекта `vacancy-dashboard`. Путь задаётся в `conftest.py`:

```python
PROJECT_PATH = Path()
```

Ожидаемая структура на диске:

```text
PycharmProjects/
├── vacancy-dashboard/         # основной проект
│   ├── app.py
│   └── parsers/
│       ├── __init__.py
│       ├── habr.py
│       └── trudvsem.py
└── job_parser_qa/             # тесты
    └── autotests/
        ├── conftest.py
        ├── requirements.txt
        ├── pytest.ini
        ├── test_parsers.py
        └── test_data_validation.py
```

## Запуск

Все тесты:

```bash
pytest
```

Только smoke-тесты (быстрая базовая проверка):

```bash
pytest -m smoke -v
```

Только быстрые тесты (без обращений к реальному API):

```bash
pytest -m "not slow"
```

Только негативные сценарии:

```bash
pytest -m negative
```

С покрытием:

```bash
pip install pytest-cov
pytest --cov=parsers --cov-report=term-missing
```

## Структура тестов

### `test_parsers.py`

**Класс `TestHabrParser`** — 8 тестов:
- Возвращает список
- Возвращает хотя бы одну вакансию для «Python»
- Обязательные поля присутствуют
- Поле `source` = «Habr Career»
- URL начинается с `https://`
- Название не пустое
- Пустой запрос не ломает парсер
- Несуществующий запрос обрабатывается корректно

**Класс `TestTrudvsemParser`** — 5 тестов:
- Возвращает список
- Обязательные поля присутствуют
- Поле `source` = «Trudvsem»
- URL начинается с `https://`
- Пустой запрос не ломает парсер

**Класс `TestSourceComparison`** — 1 тест:
- Оба парсера возвращают одинаковую структуру данных

### `test_data_validation.py`

**Класс `TestSalaryValidation`** — 3 теста:
- Зарплата — число или `None`
- Зарплата не отрицательная
- `salary_from` ≤ `salary_to`

**Класс `TestRemoteValidation`** — 2 теста:
- `remote` — булево значение
- В выборке есть оба значения (`True` и `False`)

**Класс `TestIdValidation`** — 2 теста:
- `id` — строка
- `id` уникальны

**Класс `TestSkillsValidation`** — 2 теста:
- `skills` — строка
- В `skills` нет HTML-тегов

**Класс `TestCompanyValidation`** — 2 теста:
- `company` — строка или `None`
- В `company` нет HTML-тегов

## Маркеры pytest

- `smoke` — быстрые базовые тесты, всегда должны проходить
- `slow` — тесты с реальными запросами к API (зависят от сети)
- `negative` — проверка обработки ошибок и некорректных данных

## Особенности

### Реальные запросы к API

Тесты с маркером `slow` делают **реальные HTTP-запросы** к API Habr Career и Trudvsem. Это значит:

- Тесты зависят от доступности API
- Полный прогон занимает ~3 минуты
- При недоступности API тесты упадут не по вине кода

### Зависимости

Тестовое окружение должно содержать **все зависимости основного проекта**, которые нужны для импорта парсеров. Если появляется `ModuleNotFoundError` — добавь пакет в `requirements.txt` и установи.

## Автор

Ilya Perevozchikov — [@cmetanok](https://github.com/cmetanok)