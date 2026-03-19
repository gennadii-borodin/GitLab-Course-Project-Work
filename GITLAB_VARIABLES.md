# GitLab CI/CD Variables - Рекомендации по выносу

Документ содержит список переменных из `.gitlab-ci.yml`, которые рекомендуется вынести в GitLab CI/CD Variables с указанием типа и уровня сокрытия.

## Сводная таблица переменных

| № | Переменная | Текущее значение | Тип | Masked | Protected | Environment Scope | Где используется | Обоснование / Примечания |
|---|------------|------------------|-----|--------|-----------|------------------|-------------------|--------------------------|
| **Секреты (требуют маскирования)** |
| 1 | `SPW_COOKIE_SECRET` | `some-secret-value` | Variable | ✅ Да | ✅ Рекомендуется | production | testing | Секретный ключ для подписи cookies (сессий). **КРИТИЧЕСКИ ВАЖНО**. При компрометации позволяет hijacking сессий. Заменить на `openssl rand -hex 32`. |
| 2 | `SPW_PASSWORD_SECRET` | `some-other-secret-value` | Variable | ✅ Да | ✅ Рекомендуется | production | testing | Секрет для хэширования паролей. **КРИТИЧЕСКИ ВАЖНО**. Позволяет взламывать пароли. Сгенерировать криптостойкое значение. |
| 3 | `POSTGRES_PASSWORD` | `test_password` | Variable | ✅ Да | Опционально | all / production | testing (PostgreSQL service) | Пароль к БД PostgreSQL. Даёт полный доступ к данным. Для production использовать сложный пароль. |
| 4 | `SPW_PG_PASSWORD` | `test_password` | Variable | ✅ Да | Опционально | all / production | testing | Дублирующий пароль к БД приложения. Должен совпадать с `POSTGRES_PASSWORD`. |
| **Конфигурационные (Public)** |
| 5 | `WEB_IMAGE_NAME` | `$CI_REGISTRY_IMAGE/ewb-app` | Variable | ❌ Нет | ❌ Нет | all | package, testing | Имя Docker image. Использует предопределённую `CI_REGISTRY_IMAGE`. Не требует маскирования. |
| 6 | `DOCKER_DRIVER` | `overlay2` | Variable | ❌ Нет | ❌ Нет | all | Глобально | Драйвер хранилища Docker. Зависит от инфраструктуры. Можно вынести для гибкости. |
| 7 | `DOCKER_TLS_CERTDIR` | `""` / `"/certs"` | Variable | ❌ Нет | ❌ Нет | all (разные jobs) | package, deploy-manual, stop_production | Путь к TLS сертификатам Docker. Разные значения для non-TLS и TLS режимов. |
| 8 | `DOCKER_HOST` | `tcp://docker:2375` / `tcp://docker:2376` | Variable | ❌ Нет | ❌ Нет | all (разные jobs) | package, deploy-manual, stop_production | Адрес Docker daemon. Разные порты для non-secure (2375) и secure (2376). |
| 9 | `DOCKER_CERT_PATH` | `"/certs/client"` | Variable | ❌ Нет | ❌ Нет | all (разные jobs) | deploy-manual, stop_production | Путь к client сертификатам Docker. |
| 10 | `DOCKER_TLS_VERIFY` | `0` / `1` | Variable | ❌ Нет | ❌ Нет | all (разные jobs) | deploy-manual, stop_production | Флаг включения TLS проверки Docker (0=off, 1=on). |
| 11 | `PIP_CACHE_DIR` | `$CI_PROJECT_DIR/.cache/pip` | Variable | ❌ Нет | ❌ Нет | all | Глобально | Путь к кэшу pip. Не требует маскирования. |
| 12 | `DOCKER_VERSION` | `"29.3"` | Variable | ❌ Нет | ❌ Нет | all | package, deploy-manual, stop_production | Версия Docker. **Рекомендуется вынести** для гибкости обновления. |
| 13 | `POSTGRES_DB` | `test_db` | Variable | ❌ Нет | ❌ Нет | testing | testing | Имя базы данных. Для разных сред можно использовать разные имена. |
| 14 | `POSTGRES_USER` | `test_user` | Variable | ❌ Нет | ❌ Нет | testing | testing | Имя пользователя БД. |
| 15 | `SPW_PORT` | `9999` | Variable | ❌ Нет | ❌ Нет | testing | testing | Порт веб-приложения. В production обычно 80/443. |
| 16 | `SPW_PG_HOST` | `postgres` | Variable | ❌ Нет | ❌ Нет | testing | testing | Хост PostgreSQL (имя сервиса в Docker network). |
| 17 | `SPW_PG_PORT` | `5432` | Variable | ❌ Нет | ❌ Нет | testing | testing | Порт PostgreSQL. Стандартный 5432. |
| 18 | `SPW_PG_USER` | `test_user` | Variable | ❌ Нет | ❌ Нет | testing | testing | Пользователь БД в приложении (должен = POSTGRES_USER). |
| 19 | `SPW_PG_DATABASE` | `test_db` | Variable | ❌ Нет | ❌ Нет | testing | testing | Имя БД в приложении (должно = POSTGRES_DB). |
| 20 | `SPW_MIGRATIONS_FILENAME` | `migrations.json` | Variable | ❌ Нет | ❌ Нет | testing | testing | Имя файла миграций. Параметр конфигурации. |
| 21 | `SPW_DATA_DIRECTORY` | `/app/data` | Variable | ❌ Нет | ❌ Нет | testing | testing | Путь к директории данных приложения. |
| 22 | `SPW_STATIC_FILES_DIRECTORY` | `/app/static` | Variable | ❌ Нет | ❌ Нет | testing | testing | Путь к статическим файлам приложения. |
| 23 | `SPW_COOKIE_SECRET` | `some-secret-value` | Variable | ✅ Да | ✅ Рекомендуется | production | testing | **Продублировано в секретах** (см. №1). Переменная для тестовой среды может быть другим значением. |
| 24 | `SPW_PASSWORD_SECRET` | `some-other-secret-value` | Variable | ✅ Да | ✅ Рекомендуется | production | testing | **Продублировано в секретах** (см. №2). Для тестов можно использовать другое значение. |
| 25 | `TEST_BASE_URL` | `http://web-test:$SPW_PORT` | Variable | ❌ Нет | ❌ Нет | testing | testing | Базовый URL для тестов. Зависит от порта. |

---

## Предопределённые GitLab Variables (автоматически доступны)

Эти переменные **не нужно создавать**, они предоставляются GitLab автоматически:

| Переменная | Пример значения | Используется в |
|------------|-----------------|----------------|
| `CI_REGISTRY_IMAGE` | `registry.example.com/group/project` | `WEB_IMAGE_NAME` |
| `CI_COMMIT_SHORT_SHA` | `abc1234` | Теги Docker image |
| `CI_COMMIT_BRANCH` | `main` | Условия в `package` job |
| `CI_COMMIT_REF_SLUG` | `main` | Cache key |
| `CI_PROJECT_DIR` | `/builds/group/project` | `PIP_CACHE_DIR` |
| `CI_REGISTRY` | `registry.example.com` | Docker login |
| `CI_REGISTRY_USER` | `gitlab-ci-token` | Docker login |
| `CI_REGISTRY_PASSWORD` | токен | Docker login |

**Важно**: `CI_REGISTRY_USER` и `CI_REGISTRY_PASSWORD` уже предоставляются GitLab автоматически для аутентификации в Container Registry.

---

## Рекомендации по настройке в GitLab

### 1. Порядок создания переменных

**Этап 1: Секреты (Masked + Protected)**

Зайдите в проект → **Settings** → **CI/CD** → **Variables** → **Add variable**

Для production веток:

| Key | Value | Type | Masked | Protected | Environment |
|-----|-------|------|--------|-----------|-------------|
| `SPW_COOKIE_SECRET` | `openssl rand -hex 32` | Variable | ✅ | ✅ | production |
| `SPW_PASSWORD_SECRET` | `openssl rand -hex 32` | Variable | ✅ | ✅ | production |
| `POSTGRES_PASSWORD` | `сложный_пароль_40_символов` | Variable | ✅ | ✅ | production |

Для всех веток (или отдельно для testing):

| Key | Value | Type | Masked | Protected |
|-----|-------|------|--------|-----------|
| `POSTGRES_PASSWORD` | `test_password` | Variable | ✅ | ❌ |
| `SPW_PG_PASSWORD` | `test_password` | Variable | ✅ | ❌ |
| `SPW_COOKIE_SECRET` | `test-secret-for-dev` | Variable | ✅ | ❌ |
| `SPW_PASSWORD_SECRET` | `test-secret-for-dev` | Variable | ✅ | ❌ |

**Этап 2: Конфигурационные переменные (Public)**

| Key | Value | Type | Masked | Protected |
|-----|-------|------|--------|-----------|
| `DOCKER_VERSION` | `29.3` | Variable | ❌ | ❌ |
| `DOCKER_DRIVER` | `overlay2` | Variable | ❌ | ❌ |
| `SPW_PORT` | `9999` | Variable | ❌ | ❌ |
| `POSTGRES_DB` | `test_db` | Variable | ❌ | ❌ |
| `POSTGRES_USER` | `test_user` | Variable | ❌ | ❌ |
| `SPW_PG_HOST` | `postgres` | Variable | ❌ | ❌ |
| `SPW_PG_PORT` | `5432` | Variable | ❌ | ❌ |
| `SPW_PG_USER` | `test_user` | Variable | ❌ | ❌ |
| `SPW_PG_DATABASE` | `test_db` | Variable | ❌ | ❌ |
| `SPW_MIGRATIONS_FILENAME` | `migrations.json` | Variable | ❌ | ❌ |
| `SPW_DATA_DIRECTORY` | `/app/data` | Variable | ❌ | ❌ |
| `SPW_STATIC_FILES_DIRECTORY` | `/app/static` | Variable | ❌ | ❌ |
| `TEST_BASE_URL` | `http://web-test:9999` | Variable | ❌ | ❌ |

### 2. Настройка Protected Branches

Защитите production-ветки:

1. **Repository** → **Protected branches**
2. Защитите ветки:
   - `main` (или `master`) → Разрешить merge/push только Maintainers/Owners
   - `release/*` → Аналогично
   - `production` → Аналогично
3. Для tags можно настроить: `v*.*.*` →Allowed to create: Maintainers

После этого Protected переменные будут доступны только для этих веток/тегов.

### 3. Environment-specific Variables (опционально)

Для `deploy-manual` и `stop_production` jobs можно использовать Environment Variables:

1. **Deployments** → **Environments** → **production** → **Edit**
2. Добавить переменные для environment `production`:
   - `DOCKER_TLS_CERTDIR`
   - `DOCKER_HOST`
   - `DOCKER_CERT_PATH`
   - `DOCKER_TLS_VERIFY`

Эти переменные будут доступны только при деплое в production environment.

---

## Изменения в .gitlab-ci.yml

После выноса переменных обновите файл:

```yaml
variables:
  # Удалить hardcoded значения, оставить только:
  WEB_IMAGE_NAME: $CI_REGISTRY_IMAGE/ewb-app
  DOCKER_DRIVER: $DOCKER_DRIVER  # вынести
  DOCKER_TLS_CERTDIR: $DOCKER_TLS_CERTDIR  # вынести
  DOCKER_HOST: $DOCKER_HOST  # вынести
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DOCKER_VERSION: $DOCKER_VERSION  # вынести

# В job testing удалить секреты из variables, они будут подхвачены автоматически:
testing:
  variables:
    POSTGRES_DB: $POSTGRES_DB  # вынести
    POSTGRES_USER: $POSTGRES_USER  # вынести
    POSTGRES_PASSWORD: $POSTGRES_PASSWORD  # secret (masked)
    SPW_PORT: $SPW_PORT  # вынести
    SPW_PG_HOST: $SPW_PG_HOST  # вынести
    SPW_PG_PORT: $SPW_PG_PORT  # вынести
    SPW_PG_USER: $SPW_PG_USER  # вынести
    SPW_PG_PASSWORD: $SPW_PG_PASSWORD  # secret (masked)
    SPW_PG_DATABASE: $SPW_PG_DATABASE  # вынести
    SPW_MIGRATIONS_FILENAME: $SPW_MIGRATIONS_FILENAME  # вынести
    SPW_DATA_DIRECTORY: $SPW_DATA_DIRECTORY  # вынести
    SPW_STATIC_FILES_DIRECTORY: $SPW_STATIC_FILES_DIRECTORY  # вынести
    SPW_COOKIE_SECRET: $SPW_COOKIE_SECRET  # secret (masked)
    SPW_PASSWORD_SECRET: $SPW_PASSWORD_SECRET  # secret (masked)
    TEST_BASE_URL: $TEST_BASE_URL  # вынести
```

Обратите внимание: переменные на уровне job переопределяют глобальные. После выноса в GitLab Variables они будут доступны автоматически, можно удалить из `.gitlab-ci.yml` полностью, оставив только те, что специфичны для job.

---

## Ограничения Masked Variables

GitLab накладывает ограничения на маскируемые переменные:

- ✅ Разрешены: `a-zA-Z0-9_@%+=:,./-`
- ❌ Запрещены: пробелы, `$`, `{`, `}`, `!`, `*`, `?`, другие спецсимволы
- Максимальная длина: 255 символов

Если значение не соответствует regex, установите `Masked: OFF` (но это не рекомендуется для секретов). В таком случае рассмотрите использование **File** типа или шифрование.

---

## Генерация секретов

```bash
# Сгенерировать 32-байтовый hex-ключ (64 hex символа)
openssl rand -hex 32

# Сгенерировать base64 (допускается в Masked)
openssl rand -base64 32

# Сгенерировать URL-safe base64
openssl rand -base64 32 | tr '+/' '-_' | tr -d '='
```

---

## Validation Checklist

- [ ] Все секреты (пароли, ключи) имеют `Masked: ON`
- [ ] Production-секреты имеют `Protected: ON`
- [ ] Protected branches настроены для `main`/`master`
- [ ] Variable types установлены в `Variable` (не `File`)
- [ ] Никаких секретов не осталось hardcoded в `.gitlab-ci.yml`
- [ ] Для разных сред (test/staging/prod) используются разные значения через environment scope
- [ ] `CI_REGISTRY_USER` и `CI_REGISTRY_PASSWORD` не создаются (уже предоставлены GitLab)
- [ ] Pipeline протестирован на feature-ветке (без protected vars) и на main (с protected vars)