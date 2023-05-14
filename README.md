# api_yamdb

## Техническое описание проекта YaMDb
http://127.0.0.1:8000/redoc/

## Описание

Проект YaMDB собирает отзывы пользователей на произведения (книги, фильмы, музыку). Незарегистрированные пользователи могут просматривать информацию о произведениях, жанрах и категориях произведений, а также читать отзывы и комментарии. Зарегистрированные пользователи могут оставлять отзывы и комментарии на произведения, а также выставлять оценку от 1 до 10. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Регистрация - код доступа предоставляется на переданный email
- Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен)

После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}

:exclamation: Прошу обратить внимание - наполнение базы происходит командой python/.../manage.py import_csv.
При успешном выполнении будет отчет в терминале.

## Примеры запросов к API

### Регистрация пользователя

```http
  POST api/v1/auth/signup/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. Your email|
| `username` | `string` | **Required**|

### Получение JWT-токена для завершения регистрации

```http
  POST api/v1/auth/token/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**.|
| `confirmation_code` | `string` | **Required**.| code from email


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Pavel-Leo/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env (для mac и linux)
python -m venv env (для windows)
```

```
source env/bin/activate (для mac и linux)
source venv/Scripts/activate (для windows)
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip (для mac и linux)
python -m pip install --upgrade pip (для windows)
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate (для mac и linux)
python manage.py migrate (для windows)
```

Запустить проект:

```
python3 manage.py runserver (для mac и linux)
python manage.py runserver (для windows)
```

## Авторы
- Леонтьев Павел (TeamLead) https://github.com/Pavel-Leo
- Анатолий Шабанов https://github.com/MokpoBka
- Юрий Кузнецов https://github.com/yvk3