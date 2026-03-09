FROM python:3.11-slim

WORKDIR /app

COPY tests/requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Установка PostgreSQL клиента
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["pytest", "-v", "--cov=api", "--cov-report=term-missing"]