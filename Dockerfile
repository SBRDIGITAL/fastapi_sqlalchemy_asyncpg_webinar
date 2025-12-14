# Базовый лёгкий образ Python 3.12. slim уменьшает размер и время сборки
FROM python:3.12-slim

# Все последующие команды будут выполняться из /app внутри контейнера
WORKDIR /app

# Копируем список зависимостей отдельно, чтобы кешировать слой установки pip
COPY requirements.txt .

# Устанавливаем зависимости без кеша колес, чтобы не раздувать образ
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь образа (код, alembic, настройки)
COPY . .

# Gunicorn с рабочими Uvicorn для продакшена; слушаем 0.0.0.0:8000
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]