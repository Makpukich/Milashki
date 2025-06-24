# Milashki API 
### Это серверная часть веб-приложения для управления подписками пользователей. Проект реализован на FastAPI с использованием асинхронного SQLAlchemy для работы с базой данных.

## Технологический стек
- Python 3.12
- FastAPI - веб-фреймворк
- SQLAlchemy (асинхронный) - ORM
- Uvicorn - ASGI-сервер
- Pydantic - валидация данных
- JWT - аутентификация


## Установка

Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/milashki-api.git
cd milashki-api
```

Запуск
```bash
uvicorn main:app --reload
```
После запуска API будет доступно по адресу: http://localhost:8000

## Все эндпоинты API
### Аутентификация
`POST /auth/register` - Регистрация пользователя

`POST /auth/login` - Вход в систему (получение JWT)

`GET /auth/me` - Информация о текущем пользователе

### Управление аккаунтами
`GET /accounts/` - Список всех аккаунтов

`POST /accounts/` - Создание аккаунта

`GET /accounts/<id>` - Получение аккаунта

`PUT /accounts/<id>` - Обновление аккаунта

`DELETE /accounts/<id>` - Удаление аккаунта

### `Управление подписками
`GET /subscriptions/` - Список всех подписок

`POST /subscriptions/` - Создание подписки

`GET /subscriptions/<id>` - Получение подписки

`PUT /subscriptions/<id>` - Обновление подписки

`DELETE /subscriptions/<id>` - Удаление подписки

### Пользовательские подписки
`GET /User_subs/` - Все пользовательские подписки

`POST /User_subs/` - Добавление подписки пользователю

`GET /User_subs/<user_id>/<subscription_id>` - Конкретная подписка пользователя

`GET /subscriptions/<user_id>` - Подписки конкретного пользователя

`DELETE /subscriptions/<user_id>/<sub_id>` - Удаление подписки у пользователя
