# Технологический стек

## Backend (Python)

### Core Framework
- **Bottle** (bottlepy.org) - минималистичный веб-фреймворк
  - Single-file модуль
  - Built-in development server
  - RESTful routing через декораторы
  - Plugin system для расширений

### Database
- **PostgreSQL** - мощная реляционная СУБД
  - Клиент-серверная архитектура
  - ACID-совместимость
  - Поддерживает сложные запросы, индексы, триггеры
  - Масштабируемость для production-использования

### Database Access
- **psycopg2-binary** - PostgreSQL адаптер для Python
  - Прямой доступ к PostgreSQL из Python
  - Поддержка параметризованных запросов (%s placeholders)
  - Управление транзакциями через контекстные менеджеры
  - Автоматическое преобразование типов данных

### Configuration
- **os.getenv()** - чтение переменных окружения
  - Fallback на значения по умолчанию
  - Environment-specific настройки

### Testing
- **pytest** / **unittest** (в test/ директории)
  - Импорт тестовых данных
  - Модульные тесты datastore

## Frontend (JavaScript)

### Core Framework
- **Vue.js 3** (vuejs.org) - реактивный фреймворк
  - Options API или Composition API
  - Component-based архитектура
  - Virtual DOM

### Routing
- **Vue Router 4** - SPA навигация
  - Ленивая загрузку компонентов
  - Route guards для защиты маршрутов
  - History mode

### HTTP Client
- **Axios** - promise-based HTTP клиент
  - REST API вызовы
  - Automatic JSON transformation
  - Interceptors для добавления cookies/headers

### Styling
- **Bootstrap 5** - CSS фреймворк
  - Grid система
  - Pre-built components (forms, buttons, modals)
  - Responsive design
  - Utility-first CSS

### JavaScript
- **ES6+** синтаксис
  - Arrow functions
  - Template literals
  - Destructuring
  - Modules (ES modules)

## Build & Development

### Development Tools
- Встроенный Bottle сервер (авто-reload в debug режиме)
- ngrok для публикации локального сервера
- Python venv для изоляции зависимостей
- Docker и Docker Compose для контейнеризации

### Dependencies (requirements.txt)
```
bottle==0.12.19
psycopg2-binary==2.9.9
```

### Containerization
- **Docker** - контейнеризация приложения
  - Multi-stage build не требуется (простой образ)
  - Slim образ Python 3.14 для минимального размера
  - Healthcheck для проверки доступности сервиса

- **Docker Compose** - оркестрация многоконтейнерного приложения
  - PostgreSQL 17 в отдельном контейнере
  - Изолированная сеть app-network
  - Docker volume для персистентных данных PostgreSQL
  - Зависимость web от postgres (healthcheck condition)
  - Volume mounts для кода и данных (dev-friendly)

### No Build Step
Проект не требует сборки фронтенда:
- Прямое редактирование .js и .css файлов
- Статика отдается как есть из `static/` директории
- Простота для образовательных целей

## Конфигурация

### Environment Variables

#### PostgreSQL settings
```
SPW_PG_HOST               # Хост PostgreSQL (localhost)
SPW_PG_PORT               # Порт PostgreSQL (5432)
SPW_PG_USER               # Пользователь PostgreSQL (postgres)
SPW_PG_PASSWORD           # Пароль PostgreSQL (password)
SPW_PG_DATABASE           # Имя базы данных (simple_website)
```

#### Other settings
```
SPW_MIGRATIONS_FILENAME   # Имя файла миграций
SPW_DATA_DIRECTORY        # Путь к data/ (абсолютный)
SPW_STATIC_FILES_DIRECTORY # Путь к static/ (абсолютный)
SPW_COOKIE_SECRET         # Секрет для подписи cookies
SPW_PASSWORD_SECRET       # Salt для хэширования паролей
SPW_PORT                  # Порт сервера (9999)
SPW_SESSION_TTL           # TTL сессии в минутах (10)
```

## Безопасность (упрощенная)

### Authentication
- **MD5** + salt (password_secret) - хэширование паролей
  - Примечание: MD5 криптографически сломан, используется только для образовательных целей
- **Signed cookies** - Bottle's secure cookie mechanism
  -HMAC подпись для целостности
  - Не шифрование (данные читаемы)

### Authorization
- Ролевая модель: `is_admin` флаг в users
- Проверка статуса админа в API хендлерах
- Cookies содержат metadata, но не sensitive данные

## Развертывание

### Development
```bash
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Production (не рекомендуется)
- ngrok для публичного доступа
- sqlite3 файловая БД (не для высоких нагрузок)
- Отсутствие SSL/TLS (нужен reverse proxy)

## Ограничения технологий

### Python
- Bottle не подходит для больших приложений (в отличие от Django/FastAPI)
- Нет ORM (raw SQL)
- Нет встроенной админки

### Database
- Требует запущенный PostgreSQL сервер
- Нужна настройка пользователей и прав доступа
- Менее удобна для локальной разработки без Docker

### Frontend
- Нет hot module replacement (HMR)
- Нет минификации/упаковки production build
- Нет TypeScript

## Потенциальные улучшения

### Security
- Заменить MD5 на bcrypt или Argon2
- Использовать JWT вместо cookies
- HTTPS в production

### Architecture
- Добавить полноценный ORM (SQLAlchemy)
- Миграции через Alembic/Aerich
- Microservices: разделить auth, userdata, things

### Frontend
- TypeScript вместо plain JS
- Vue CLI или Vite для сборки
- Jest/Vitest для unit тестов
- Cypress для E2E тестов

### DevOps
- Docker и Docker Compose для локального development и deployment
- CI/CD pipeline (для будущего implementation)
- Production WSGI сервер (gunicorn/uvicorn) - рекомендуется для production
- Reverse proxy (nginx) с SSL termination - рекомендуется для production
