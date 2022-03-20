# Requests API

### ТЗ
Реализовать CRUD сервис, который обрабатывает, принимает и
хранит тела запросов, а также считает количество одинаковых запросов. Тела
запросов хранятся по ключу (строка).
Ключ генерируется из параметров тела запроса, методом “ключ+значение”, после
чего кодируется в base64.

### Stack

- Tornado
- Databases
- SQLAlchemy
- Alembic
- docker, docker-compose

### Deploy
*local*
- запустить приложение и БД в докере:
`docker-compose up -d`

*dev*

todo

### TODO
 - tests
 - nginx config + tornado multiprocesses
 - linters
 - poetry
