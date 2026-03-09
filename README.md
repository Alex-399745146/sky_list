# SKY_LIST

---

## Курсовая работа 

По итогам обучения модуля ООП.

---

Консольное приложение на Python для получения данных о самолётах из API
nominatim.openstreetmap.org и opensky-network.org, фильтрации, сортировки и
сохранения результатов в JSON.

* [API nominatim openstreetmap](https://nominatim.openstreetmap.org/ui/search.html)
* [API opensky network](https://opensky-network.org/)

---

## 1. Описание проекта

Программа с терминальным меню, которая собирает данные о самолётах в воздушных
пространствах выбранных пользователем стран.

### 1.1. Стек технологий

```text
#magic_method #requests #API #pandas #ООП (абстрактные классы, множественное наследование)
```


### 1.2. API key

Сервисы используют открытый API, ключи не требуются, что упрощает запуск приложения.

---

## 2. Установка и запуск

### 2.1. Установка

```bash
git clone https://github.com/<твой-логин>/sky_list.git
```

```bash
cd sky_list
```

```bash
poetry install
```
### 2.2. Запускаем
```bash
poetry run python main.py
```

---

## 3. Использование

```markdown
После запуска программа запросит:
```
1. Название страны для запроса к API.
2. Количество самолётов для вывода в топ N.
3. Список стран регистрации (через пробел) для фильтрации.
4. Диапазон высот (например, 1000-15000).

Результат выводится таблицей в консоль и сохраняется без дубляжа в `data/aeroplanes.json`.

---

## 4. Структура проекта

- `src/api_clients.py` — работа с внешними API (Nominatim, OpenSky).
- `src/airplanes.py` — классы `BaseAeroplane` и `Aeroplane`, фильтрация и сравнение.
- `src/processing.py` — классы работы с JSON-файлом.
- `main.py` — точка входа, логика взаимодействия с пользователем.
- `tests/` — тесты на pytest.

---

## 5. Технологии

```markdown
* Python 3.13
* Poetry
* requests, pytest, pytest-cov, mypy, flake8, black, isort
```
### 5.1. Тестирование и проверка стиля

```bash
poetry run pytest
```
```bash
poetry run pytest --cov=src
````
```bash
poetry run mypy .
```
```bash
poetry run flake8 .
```

---

## 6. Лицензия

Учебная работа по итогу окончания учебного модуля по ООП

### 6.1. Автор

Александр Бачевский (Alex Bachevskiy)

Telegram: [@bachevskiyaa](@bachevskiyaa)

Email: [bachevskiyaa@bk.ru](bachevskiyaa@bk.ru)

Email (Gmail): [bachevskiiaa@gmail.com](bachevskiiaa@gmail.com)

### 6.2. Лицензия
Учебный проект.

---