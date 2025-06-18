# Microblog API

Microblog API — это RESTful-сервис микроблогов, разработанный на FastAPI. 

#### Сервис предназначен для корпоративного использования и реализует базовые функции Twitter: 
- публикация твитов, подписки, лайки, лента, загрузка медиафайлов и авторизация по API-ключу.

## Возможности

- Авторизация по API-ключу
- Создание и удаление твитов
- Лайки и дизлайки твитов
- Подписка и отписка от других пользователей
- Лента твитов по подпискам, сортированная по популярности
- Загрузка и хранение изображений
- Swagger UI-документация на /docs
- Развёртывание через Docker Compose

---

## Структура проекта

```
microblog/
├── app/
│   ├── main.py           # Точка входа, инициализация FastAPI
│   ├── models.py         # SQLAlchemy-модели
│   ├── schemas.py        # Pydantic-схемы
│   ├── crud.py           # Логика работы с базой данных
│   ├── auth.py           # Авторизация по API-ключу
│   ├── deps.py           # Зависимости FastAPI
│   ├── database.py       # Подключение к PostgreSQL через SQLAlchemy
│   └── routes/           # Роуты API:
│       ├── tweets.py
│       ├── users.py
│       └── medias.py
├── .env                  # Переменные окружения
├── Dockerfile            # Сборка контейнера
├── docker-compose.yml    # Описание сервисов (БД + API)
├── requirements.txt      # Python-зависимости
└── README.md             # Описание проекта
```

## Установка и запуск

### Требования

- Docker
- Docker Compose

### Инструкция

```bash
# Клонировать репозиторий:
git clone https://your.git.repo/microblog-api.git
cd microblog-api

# Запустить сборку и приложение:
docker-compose up --build

# После запуска:
# Swagger: http://localhost:8000/docs
# Приложение: http://localhost:8000


```
### Завершение работы

```bash
# Остановить и удалить контейнеры:
docker-compose down
```

---


## Авторизация


### Тестовые пользователи

| Имя пользователя | API-Key     |
|------------------|-------------|
| Alice            | alice-key   |
| Bob              | bob-key     |

```http
# Пример заголовка:
api-key: alice-key
```

---

## Основные маршруты (endpoint'ы)

| Метод  | Путь                          | Описание                                 |
|--------|-------------------------------|------------------------------------------|
| POST   | `/api/tweets`                | Создать твит                             |
| DELETE | `/api/tweets/{id}`           | Удалить твит                             |
| POST   | `/api/tweets/{id}/likes`     | Поставить лайк                           |
| DELETE | `/api/tweets/{id}/likes`     | Убрать лайк                              |
| GET    | `/api/tweets`                | Получить ленту твитов                    |
| POST   | `/api/medias`                | Загрузить изображение                    |
| GET    | `/api/users/me`              | Получить текущий профиль пользователя    |
| GET    | `/api/users/{id}`            | Получить профиль пользователя по ID      |
| POST   | `/api/users/{id}/follow`     | Подписаться на пользователя              |
| DELETE | `/api/users/{id}/follow`     | Отписаться от пользователя               |

---


---

## Переменные окружения

Файл `.env` в корне проекта:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=twitterdb
DATABASE_URL=postgresql://postgres:postgres@db:5432/twitterdb
```

---

