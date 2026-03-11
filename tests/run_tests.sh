#!/bin/bash

# Создание директорий для результатов Allure и отчета о покрытии
mkdir -p allure-results allure-report coverage-report

echo "Запуск инфраструктуры через docker-compose..."
docker-compose up -d

echo "Ожидание готовности веб-сервера..."
# Ждём пока healthcheck станет healthy
for i in {1..30}; do
  status=$(docker inspect -f "{{.State.Health.Status}}" webapp 2>/dev/null || echo "starting")
  if [ "$status" = "healthy" ]; then
    echo "Веб-сервис готов"
    break
  fi
  echo "Веб-сервис не готов (статус: $status), ждём... ($i/30)"
  sleep 2
done

echo "Сборка контейнера с тестами..."
docker build -f tests/Dockerfile -t api-tests .

echo "Запуск тестов в контейнере..."
docker run \
  --network app-network \
  -v "$(pwd)/allure-results:/app/allure-results" \
  -v "$(pwd)/allure-report:/app/allure-report" \
  -v "$(pwd)/coverage-report:/app/coverage-report" \
  -e TEST_BASE_URL=http://web:80 \
  api-tests

echo "Тесты завершены"
echo "Allure отчёт сгенерирован в: allure-report/index.html"
echo "HTML отчёт о тестовом покрытии сгенерирован в: coverage-report/index.html"
echo "Для просмотра откройте соответствующие файлы в браузере"

echo "Остановка инфраструктуры..."
docker-compose down