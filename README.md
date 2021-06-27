Django Postgres Row-Level-Security
==================================

Building multi-tenant application with using database "shared" pattern.

## Concepts

* Avoid multiple schema/database for high-performance.
* Protecting data from other tenant.

references:

* https://pganalyze.com/blog/postgres-row-level-security-django-python

## Usage

### boot

```
$ docker-compose up
```
### DB migration

```
$ docker-compose exec dj python3 manage.py migrate
```

### access

* http://localhost:8000/admin/
    * Tenant1: ID/PW: haru
    * Tenant2: ID/PW: terada
    * Admin: ID/PW: admin

### containers

* dj (django)
    * http://localhost:8000/
* db (postgres)
    * ID/password: `root`/`root`

### DB console
```
$ docker-compose exec db psql -U db
```
