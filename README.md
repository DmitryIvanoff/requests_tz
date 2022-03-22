# Requests API

### ТЗ
Реализовать CRUD сервис, который обрабатывает, принимает и
хранит тела запросов, а также считает количество одинаковых запросов. Тела
запросов хранятся по ключу (строка).
Ключ генерируется из параметров тела запроса, методом “ключ+значение”, после
чего кодируется в base64.

### Stack

- [Tornado]
- [Databases]
- [SQLAlchemy]
- [Alembic]
- [Marshmallow]
- docker, docker-compose

### Deploy
**local**
- запустить приложение и БД в докере:
```shell
$ docker-compose up -d
```

**dev**

todo

### TODO
 - tests
 - nginx config + tornado multiprocesses
 - linters, formatters
 - poetry
 - load testing (script)

[Alembic]: https://alembic.sqlalchemy.org/en/latest/
[psycopg2]: https://www.psycopg.org/
[Databases]: https://github.com/encode/databases
[asyncpg]: https://github.com/MagicStack/asyncpg
[aiopg]: https://github.com/aio-libs/aiopg
[aiosqlite]: https://github.com/omnilib/aiosqlite
[Tornado]: https://github.com/tornadoweb/tornado
[SQLAlchemy]: https://docs.sqlalchemy.org/en/latest/core/
[Marshmallow]: https://github.com/marshmallow-code/marshmallow