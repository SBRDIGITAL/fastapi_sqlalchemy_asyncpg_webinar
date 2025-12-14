![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-orange)
![asyncpg](https://img.shields.io/badge/Driver-asyncpg-lightgrey)
![Alembic](https://img.shields.io/badge/Migrations-Alembic-yellow)
![Docker](https://img.shields.io/badge/Docker-compose-blue)
![Pytest](https://img.shields.io/badge/Tests-pytest-purple)

# FastAPI + SQLAlchemy (async) + asyncpg

Небольшой учебный сервис с асинхронным FastAPI, SQLAlchemy 2.x и драйвером asyncpg. Включает конфигурацию через `.env`, миграции Alembic, docker-compose и минимальный набор тестов.

## Стек
- FastAPI
- Pydantic / pydantic-settings
- SQLAlchemy 2.x (async) + asyncpg
- Alembic
- Docker / docker-compose
- Pytest

## Быстрый старт
0) [Базу данных возьми тут](https://github.com/SBRDIGITAL/postgrocker_18.git)
1) Скопировать пример окружения и заполнить значения:

```bash
cp .env.example .env  # если примера нет, см. блок ниже
```

2) Собрать и поднять сервисы:

```bash
docker compose up --build
```

3) Применить миграции (если нужно вручную):

```bash
docker compose exec app alembic upgrade head
```

4) API доступно по `http://localhost:8000` (см. переменные `API_HOST`/`API_PORT`).

## Переменные окружения (.env)
Используются pydantic-settings. Ключевые переменные (см. `app/config/config_reader.py`):
- `API_HOST`, `API_PORT` — хост и порт FastAPI.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` — доступ к БД.
- `DB_ECHO`, `DB_POOL_SIZE`, `DB_MAX_OVERFLOW` — поведение SQLAlchemy.
- `ENV` — окружение (`development`/`production`).

### Пример .env для разработки
```
ENV=development
API_HOST=127.0.0.1
API_PORT=8000

POSTGRES_DB=postgrocker_db
POSTGRES_USER=postgrocker_user
POSTGRES_PASSWORD=postgrocker_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DB_ECHO=True
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### Пример .env для продакшена (docker-compose)
```
ENV=production
API_HOST=0.0.0.0        # внутри контейнера
API_PORT=8000           # наружу пробрасывается в docker-compose

POSTGRES_DB=postgrocker_db
POSTGRES_USER=postgrocker_user
POSTGRES_PASSWORD=postgrocker_password
POSTGRES_HOST=postgrocker_18   # имя контейнера/сервиса БД в docker сети
POSTGRES_PORT=5432

DB_ECHO=False           # меньше лишних логов
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

## Dev / Prod через docker-compose
- Файл `Docker-compose.yml` читает `.env` и поверх него задаёт переменные в секции `environment`.
- Для дев-режима: держите `ENV=development` и `DB_ECHO=True` в `.env`, запускайте `docker compose up --build`. Порт пробрасывается на `127.0.0.1:${API_PORT}`.
- Для прод-режима: установите `ENV=production`, `DB_ECHO=False`, убедитесь, что `POSTGRES_HOST` указывает на контейнер/хост с БД в нужной сети. При необходимости поменяйте `API_PORT` в `.env`.
- В проде логи приложения пишутся в смонтированную папку `./app_docker_logs` (см. volumes в compose).

## База данных и миграции
- Базовая модель и сессия — в `app/database`.
- Миграции Alembic — каталог `alembic/versions/`.
- Запуск Alembic внутри контейнера:
  - `docker compose exec app alembic upgrade head` — применить миграции.
  - `docker compose exec app alembic downgrade -1` — откат на одну версию.
  - `docker compose exec app alembic revision --autogenerate -m "message"` — сгенерировать новую миграцию (модели должны быть актуальны).
- Локальный запуск (без контейнера): активируйте venv, убедитесь что переменные окружения выставлены как в `.env`, затем выполняйте команды `alembic ...` из корня проекта.
- Файл `alembic.ini` и `alembic/env.py` берут строку подключения из настроек приложения (см. `app/config/config_reader.py`).

## Структура проекта

```
app/
	api/
		dependencies/   # Depends для DAO и сессии БД
		exceptions/     # Кастомные HTTP-исключения
		dao/            # Слой доступа к данным
		v1/
			routes/       # Маршруты FastAPI v1
			models/       # Pydantic модели запросов/ответов v1
	config/           # Чтение .env и константы
	database/         # Подключение к БД и ORM-модели
	schemas/          # Базовые схемы Pydantic
alembic/            # Конфигурация и версии миграций
Dockerfile
Docker-compose.yml
main.py             # Точка входа FastAPI
pyproject.toml / requirements.txt
```

## API (v1)
- `GET /v1/healthcheck` — проверка работоспособности.
- `POST /v1/users` — создать пользователя.
- `GET /v1/users` — список пользователей.
- `GET /v1/users/{id}` — получить пользователя по id.

## Тесты

```bash
pytest
```

## Полезное
- Логика конфигурации: `app/config/config_reader.py`.
- Pydoc добавлен к маршрутам, схемам, зависимостям и исключениям для быстрой навигации.
