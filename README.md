# small social application

Simple RESTful API for a social networking application. 
Authentication/authorization with JWT tokens. 
Storage content and user data in PostgreSQL.
Migrations with Alembic. Gunicorn start application in docker-compose.

## Dependencies
* Python 3.10
* FastApi
* SQLAlchemy(async)
* PostgreSQL
* Alembic
* JWT
* Gunicorn
* Docker

## For start application

```commandline
docker-compose up --build
```

### [OpenAPI](http://localhost:8000/api/openapi#/) documentation


## tests

* Pytest
* Docker-compose

### For test in test directory use:

```commandline
docker-compose up --build
```
