#!/bin/bash

echo "Сборка контейнера с тестами..."
docker build -f tests/Dockerfile -t api-tests .

echo "Запуск тестов в контейнере..."
docker run --network host \
  -e DATABASE_URL=postgresql://postgres:password@localhost:5432/simple_website \
  -e COOKIE_SECRET=test-secret \
  -e SESSION_TTL=3600 \
  api-tests

echo "Тесты завершены"