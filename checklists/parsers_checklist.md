# Чек-лист — парсеры

## Habr Career

- [x] API доступен: `career.habr.com/api/frontend/vacancies`
- [x] Запрос «Python» возвращает вакансии
- [x] Запрос «QA» возвращает вакансии
- [x] Поле `source` = «Habr Career»
- [x] Поле `remote` определяется
- [x] Поле `salary_from`/`salary_to` — числа или None
- [x] Поле `url` начинается с https://
- [x] Поле `skills` — строка через запятую

## Trudvsem

- [x] API доступен: `opendata.trudvsem.ru/api/v1/vacancies`
- [x] Запрос «Python» возвращает вакансии
- [x] Поле `source` = «Trudvsem»
- [x] Поле `remote` определяется по `employment_type`
- [x] Поле `url` начинается с https://
- [x] Поле `requirements` (навыки) не пустое

## Обработка ошибок

- [x] Таймаут API не ломает приложение
- [x] 403/500 от API обрабатывается
- [x] Пустой ответ обрабатывается
- [x] Некорректный JSON не ломает парсер