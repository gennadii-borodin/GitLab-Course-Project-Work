# CI/CD пайплайн для веб-приложения

## Обзор

CI/CD пайплайн для Python веб-приложения. Автоматизирует сборку Docker-образа, статический анализ, тестирование и ручной депLOY на production.

## Этапы и задания

**4 этапа:**
1. **package** — сборка и публикация Docker-образа в GitLab Container Registry
2. **static-analysis** — статический анализ кода (параллельно: безопасность + линтинг)
3. **test** — тестирование в изолированном окружении + генерация отчётов
4. **deploy-manual** — ручной депLOY только из ветки main

**Задания:**
- `static-security-analysis` — анализ безопасности (Bandit)
- `static-code-analysis` — линтинг кода (Ruff)
- `package` — сборка Docker-образа с multi-stage кэшированием
- `testing` — интеграционные тесты в Docker Compose
- `generate_and_publish_report` — Allure HTML-отчёт
- `deploy-manual` — деплой на production через SSH

## Архитектурные особенности

- **Docker-in-Docker** для сборки образов
- **Multi-stage кэширование** слоёв Docker и pip
- **Изоляция тестов** через Docker Compose (отдельная БД)
- **Автоматическое ожидание** готовности сервисов
- **Ручной деплой** с подтверждением в GitLab UI
- **Шаблоны** `.python-base` и `.dind-image` для повторного использования
- **Кэширование** артефактов (срок хранения 1 неделя)
- **Гибкость**: `allow_failure` для анализа и тестов

## Требуемые GitLab Variables

**Обязательные:**
- `WEB_APP_NAME` — имя приложения в Registry
- `SSH_PRIVATE_KEY`, `DEPLOY_HOST`, `SSH_USER`, `DEPLOY_PATH` — деплой
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — база данных

**Автоматически предоставляемые GitLab:**
- `CI_REGISTRY`, `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`

**Передаются на сервер в .env:**
- `SPW_PG_HOST`, `SPW_PG_PORT`, `SPW_PG_USER`, `SPW_PG_PASSWORD`, `SPW_PG_DATABASE`
- `SPW_MIGRATIONS_FILENAME`, `SPW_DATA_DIRECTORY`, `SPW_STATIC_FILES_DIRECTORY`
- `SPW_COOKIE_SECRET`, `SPW_PASSWORD_SECRET`, `SPW_PORT`, `SPW_SESSION_TTL`
