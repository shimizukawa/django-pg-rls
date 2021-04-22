Django Postgres Row-Level-Security
==================================

## boot

```
$ docker-compose up
```

## containers

* rls (django)
    * http://localhost:8000/
* db (postgres)
    * ID/password: `root`/`root`
    
## DB migration

```
$ docker-compose exec rls python3 manage.py migrate
```
