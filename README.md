# Микросервис для работы с балансом пользователей
## Описание
Проект выполнен в рамках тестового задания [AvitoTech](https://github.com/avito-tech/autumn-2021-intern-assignment).

Стек технологий: Python, Django Rest Framework, Docker, Gunicorn, Nginx, PostgreSQL, Pytest.
#### Проблема:
В нашей компании есть много различных микросервисов. Многие из них так или иначе хотят взаимодействовать с балансом пользователя. На архитектурном комитете приняли решение централизовать работу с балансом пользователя в отдельный сервис.

#### Задача:
Необходимо реализовать микросервис для работы с балансом пользователей (зачисление средств, списание средств, перевод средств от пользователя к пользователю, а также метод получения баланса пользователя). Сервис должен предоставлять HTTP API и принимать/отдавать запросы/ответы в формате JSON.

## Установка
#### Шаг 1. Проверьте установлен ли у вас Docker
Прежде, чем приступать к работе, необходимо знать, что Docker установлен. Для этого достаточно ввести:
```bash
docker -v
```
Или скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop) для Mac или Windows. [Docker Compose](https://docs.docker.com/compose) будет установлен автоматически. В Linux убедитесь, что у вас установлена последняя версия [Compose](https://docs.docker.com/compose/install/). Также вы можете воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).

#### Шаг 2. Клонируйте репозиторий себе на компьютер
Введите команду:
```bash
git clone https://github.com/DenisSivko/autumn-2021-intern-assignment.git
```

#### Шаг 3. Создайте в клонированной директории файл .env
Пример:
```bash
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='apiavito@gmail.com'
EMAIL_HOST_PASSWORD='password'
EMAIL_PORT=587
```

#### Шаг 4. Запуск docker-compose
Для запуска необходимо выполнить из директории с проектом команду:
```bash
docker-compose up -d
```

#### Шаг 5. База данных
Создаем и применяем миграции:
```bash
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
```

#### Шаг 6. Подгружаем статику
Выполните команду:
```bash
docker-compose exec web python manage.py collectstatic --no-input 
```

#### Шаг 7. Заполнение базы тестовыми данными
Для заполнения базы тестовыми данными вы можете использовать файл fixtures.json, который находится в infra_sp2. Выполните команду:
```bash
docker-compose exec web python manage.py loaddata fixtures.json
```

#### Шаг 8. Запуск тестов
Выполните команду:
```bash
docker-compose exec web python manage.py test -v 2
```
Или команду:
```bash
docker-compose exec web pytest
```

#### Документация
Документация к API доступна по адресу:
```json
http://127.0.0.1/redoc/
http://127.0.0.1/swagger/
```

#### Другие команды
Создание суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Остановить работу всех контейнеров:
```bash
docker-compose down
```

Для пересборки и запуска контейнеров воспользуйтесь командой:
```bash
docker-compose up -d --build 
```

Мониторинг запущенных контейнеров:
```bash
docker stats
```

Останавливаем и удаляем контейнеры, сети, тома и образы:
```bash
docker-compose down -v
```

## Примеры
Для формирования запросов и ответов использована программа [Postman](https://www.postman.com/).

### Получаем confirmation_code
Отправляем POST-запрос на адрес `http://127.0.0.1/api/v1/auth/email/` 

- Обязательное поле: `email`

```json
POST http://127.0.0.1/api/v1/auth/email/
Content-Type: application/json

{
    "email": "<EMAIL>"
}
```
Код подтверждения будет отправлен на e-mail адрес.
***
### Получаем token
Отправляем POST-запрос для получения JWT-токена на адрес `http://127.0.0.1/api/v1/auth/token/`.
- Обязательное поле: `email`,
- Обязательное поле: `confirmation_code`
```json
POST http://127.0.0.1/api/v1/auth/token/
Content-Type: application/json

{
    "email": "<EMAIL>",
    "confirmation_code": "<CONFIRMATION CODE>"
}
```
***
### Профиль
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/users/me/`.
```json
GET http://127.0.0.1/api/v1/users/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Редактирование информации в профиле
Отправляем PATCH-запрос на адрес `http://127.0.0.1/api/v1/users/me/`.
```json
PATCH http://127.0.0.1/api/v1/users/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json

{
    "first_name": "<NAME>",
    "last_name": "<SURNAME>",
    "username": "<USERNAME>",
    "bio": "<INFO ABOUT YOURSELF>"
}
```
***
### Создание счёта
Отправляем POST-запрос на адрес `http://127.0.0.1/api/v1/accounts/`.
```json
POST http://127.0.0.1/api/v1/accounts/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Информация о счёте
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/accounts/`.
```json
GET http://127.0.0.1/api/v1/accounts/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Получение баланса в отличной от рубля валюте
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/accounts/?currency={CURRENCY}`.
```json
GET http://127.0.0.1/api/v1/accounts/?currency={CURRENCY}
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Список пополнений счёта
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/actions/`.
```json
GET http://127.0.0.1/api/v1/actions/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Пополнение счёта
Отправляем POST-запрос на адрес `http://127.0.0.1/api/v1/actions/`.
```json
POST http://127.0.0.1/api/v1/actions/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json

{
    "account": "<YOUR ID ACCOUNT>",
    "amount": "<AMOUNT>"
}
```
***
### Список услуг
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/services/`.
```json
GET http://127.0.0.1/api/v1/services/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Приобретение услуги
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/services/{id}/purchase/`.
```json
GET http://127.0.0.1/api/v1/services/{id}/purchase/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Список приобретенных услуг
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/transactions/`.
```json
GET http://127.0.0.1/api/v1/transactions/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Список денежных переводов с вашего аккаунта
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/transfers/`.
```json
GET http://127.0.0.1/api/v1/transfers/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Список денежных переводов на ваш аккаунт
Отправляем GET-запрос на адрес `http://127.0.0.1/api/v1/transfers/to_my_account/`.
```json
GET http://127.0.0.1/api/v1/transfers/to_my_account/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json
```
***
### Перевод денежных средств
Отправляем POST-запрос на адрес `http://127.0.0.1/api/v1/transfers/`.
```json
POST http://127.0.0.1/api/v1/transfers/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDIyOTU2LCJqdGkiOiJhOThhNzY5ZjM3MjQ0OGI2YjNkZmU2ZWZhZTk3ZjQ5MyIsInVzZXJfaWQiOjN9.up2BFy3C_Yd3WrsiZLO3EQbZ5DZMqqmfAOXF0lrlIw0
Content-Type: application/json

{
    "from_account": "<ID ACCOUNT>",
    "to_account": "<ID ACCOUNT>",
    "amount": "<AMOUNT>"
}
```
