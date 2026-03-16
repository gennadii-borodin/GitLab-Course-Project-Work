FROM python:3.14-slim

# Установка зависимостей для тестирования
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание директорий
RUN mkdir -p /app/logs

# Настройка переменных окружения для тестов
ENV SPW_PG_HOST=postgres
ENV SPW_PG_PORT=5432
ENV SPW_PG_USER=postgres
ENV SPW_PG_PASSWORD=
ENV SPW_PG_DATABASE=postgres
ENV SPW_MIGRATIONS_FILENAME=migrations.json
ENV SPW_DATA_DIRECTORY=/app/data
ENV SPW_STATIC_FILES_DIRECTORY=/app/static
ENV SPW_COOKIE_SECRET=
ENV SPW_PASSWORD_SECRET=
ENV SPW_PORT=8080
ENV SPW_SESSION_TTL=10

# Запуск приложения
CMD ["python3", "main.py"]