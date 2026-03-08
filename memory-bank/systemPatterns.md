# Архитектурные паттерны

## Обзор архитектуры
Проект следует классической **MVC (Model-View-Controller)** архитектуре с REST API:

```
┌─────────────────┐
│   Presentation  │ ← SPA на Vue.js (HTML/CSS/JS)
│     Layer       │    - static/ файлы
├─────────────────┤    - components/
│   API Layer     │ ← Bottle REST endpoints
│   (Controllers) │    - api/*.py модули
├─────────────────┤
│ Business Layer  │ ← Логика работы с данными
│  (Services)     │    - datastore/*.py модули
├─────────────────┤
│   Data Layer    │ ← SQLite база данных
│  (Models)       │    - Database tables
└─────────────────┘
```

## Ключевые паттерны

### 1. MVC (Model-View-Controller)
- **Model**: `datastore/` -直接 работа с БД (users.py, things.py, connection.py)
- **View**: `static/` - HTML страницы с Vue.js компонентами
- **Controller**: `api/` - REST эндпоинты, обработка HTTP запросов

### 2. Repository / Data Access Layer
Модули в `datastore/` инкапсулируют доступ к данным:
- `connection.py` - управление подключениями к SQLite
- `store.py` - общие операции (миграции, импорт данных)
- `users.py`, `things.py` - бизнес-логика для конкретных доменов

### 3. Singleton (Конфигурация)
`data/config.py` реализует синглтон для глобальной конфигурации:
- Единственный экземпляр `Config.config`
- Чтение из переменных окружения с fallback на значения по умолчанию
- Централизованное управление настройками

### 4. Plugin Architecture (Bottle)
Использование `bottle_sqlite.SQLitePlugin`:
- Автоматическое подключение БД к каждому хендлеру
- Инъекция `db` параметра в функции-обработчики

### 5. Cookie-based Authentication
Аутентификационная система:
- Подписанные cookies с типом `account`
- Хранение сессионных данных (username, client-ip, real-name)
- Server-side проверка через БД
- MD5 хэширование паролей с salt (password_secret)

### 6. Migration-based Database Evolution
Система миграций через JSON файл:
- `migrations.json` содержит последовательные SQL миграции
- Версионирование схемы БД через таблицу `migrations`
- Автоматическое применение только новых миграций

### 7. SPA (Single Page Application)
Фронтенд архитектура:
- Vue.js 3 компонентный подход
- Vue Router 4 для клиентской навигации
- Axios для REST API вызовов
- Bootstrap 5 для UI компонентов

## Структура данных

### База данных (SQLite)
4 основные таблицы:
1. **users** - пользователи (id, firstname, lastname, is_admin, created_at)
2. **auth_methods** - методы аутентификации (user_id, username, password, type)
3. **things** - пользовательские данные (id, name)
4. **migrations** - история миграций (version, comment, migration_date)

## Компоненты системы

### Backend (Python/Bottle)
- **main.py**: точка входа, инициализация плагинов, запуск сервера
- **api/login.py**: регистрация и аутентификация
- **api/user.py**: управление пользователями (админка)
- **api/things.py**: управление вещами (CRUD)
- **api/static.py**: отдача статики
- **api/errors.py**: обработка ошибок

### Frontend (Vue.js)
Компоненты в `static/scripts/components/`:
- `LoginForm.js` - форма входа
- `RegistrationForm.js` - форма регистрации
- `ThingList.js` - список вещей
- `Thing.js` - единичная сущность вещи
- `CurrentUserInfo.js` - информация о текущем пользователе

## Потоки данных

### Регистрация/Логин
1. Фронтенд отправляет POST /register или /login
2. API валидирует данные, проверяет БД
3. При успехе: создает/находит пользователя
4. Устанавливает подписанную cookie
5. Возвращает JSON статус

### Администрирование
1. Админ заходит (флаг is_admin в users)
2. Доступ к странице /admin
3. API проверяет cookie и админский статус
4. Показывает/управляет пользователями

### CRUD операции с Things
1. Пользователь авторизован (cookie валидна)
2. Vue Router направляет на нужную страницу
3. Axios вызывает API endpoints (/api/things)
4. Store обновляет БД через datastore.things
5. Результат отдается в JSON