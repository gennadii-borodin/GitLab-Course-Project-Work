# Технологический стек

## Backend (Python)

### Core Framework
- **Bottle** (bottlepy.org) - минималистичный веб-фреймворк
  - Single-file модуль
  - Built-in development server
  - RESTful routing через декораторы
  - Plugin system для расширений

### Database
- **SQLite3** (stdlib) - встроенная реляционная БД
  - Файловая БД (test1.db)
  - ACID-совместимость
  - Подходит для prototyping и low-traffic приложений

### Database Access
- **bottle_sqlite** - Bottle plugin для SQLite
  - Автоматическое подключение к БД
  - Инъекция `db` объекта в хендлеры
  - Управление транзакциями

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

### Dependencies (requirements.txt)
Потенциальные зависимости:
```
bottle
bottle-sqlite
```
ИЛИ все зависимости могут быть inline если используется встроенный модуль sqlite3.

### No Build Step
Проект не требует сборки фронтенда:
- Прямое редактирование .js и .css файлов
- Статика отдается как есть из `static/` директории
- Простота для образовательных целей

## Конфигурация

### Environment Variables
```
SPW_DATABASE_FILENAME     # Имя файла БД
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
- SQLite: одна запись на запись (no concurrent writes)
- Нет user/password аутентификации БД
- Ограниченный размер (обычно 2GB)

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
- Мigarations через Alembic/Aerich
- Microservices: разделить auth, userdata, things

### Frontend
- TypeScript вместо plain JS
- Vue CLI или Vite для сборки
- Jest/Vitest для unit тестов
- Cypress для E2E тестов

### DevOps
- Docker контейнеризация
- CI/CD pipeline
- Production WSGI сервер (gunicorn/uvicorn)
- Reverse proxy (nginx)