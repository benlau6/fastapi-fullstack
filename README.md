# fastapi-crud-users-permission

## Introduction
A FastAPI project template with CRUD, authentication, authorization, documentation, and testing.

### Features
* [X] Authentication with registration, login, password reset and email verification 
* [X] Authorization per user, per row, per route
* [X] ORM support 
* [X] JWT and cookie authentication backends
* [X] Automatic OpenAPI documentation
* [X] Test Automation

### Thanks to
* [fastapi](https://github.com/tiangolo/fastapi) ([doc](https://fastapi.tiangolo.com/)) for one of the best api framework in python. Don't skip the doc if you just knew it. It is perfectly written.
* [fastapi-users](https://github.com/frankie567/fastapi-users) ([doc](https://frankie567.github.io/fastapi-users/)) for comprehensive user model.
* [fastapi-permission](https://github.com/holgi/fastapi-permissions) ([doc](https://github.com/holgi/fastapi-permissions/blob/master/README.md)) for row-based security control.
* [fastapi-crudrouter](https://github.com/awtkns/fastapi-crudrouter) ([doc](https://fastapi-crudrouter.awtkns.com/)) for quick crud development.
* [tortoise-orm](https://github.com/tortoise/tortoise-orm) ([doc](https://tortoise-orm.readthedocs.io/en/latest/)) for database orm, you can switch to any other orms for new features without any problems. However, if you want to switch it for features in use, e.g. fastapi-users and fastapi-permission. Re-configuration of pytest is needed.
* [traefik](https://github.com/traefik/traefik) ([doc](https://doc.traefik.io/traefik/)) for reverse proxy and payload size limiting.
* [pytest](https://github.com/pytest-dev/pytest) ([doc](https://docs.pytest.org/)) for testing

### Notes
Some fastapi third party libraries are selected because they earned many stars, well developed and maintained. Many new features may be added in without any efforts. But the most of the features you may use can acutally be rebuilt with some efforts. So if for educational purpose, to know what has been done, I recommend to build from scratch with only FastAPI. 

You may want to check [fastapi-mongo-oauth](https://github.com/benlau6/fastapi-mongo-oauth), which is built from scratch with mongo.

You may also wanna check [fastapi-pynamodb-lambda-simple](https://github.com/benlau6/fastapi-pynamodb-lambda-simple.git) for using FastAPI on AWS \
(or [fastapi-pynamodb-lambda-versioning](https://github.com/benlau6/fastapi-pynamodb-lambda-versioning) for better project file structure)

## Setup
Reminder: All project development, testing, and deployment are done in windows10/11. docker-compose.yml may need to be changed for linux/mac environment

### To build and run the container
#### get to the workdir
```
git pull https://github.com/benlau6/fastapi-crud-users-permission.git
cd fastapi-crud-users-permission
```
#### single server for dev/test (server auto restart after py code change)
```
docker-compose down ; docker-compose up --build
```
#### multiple servers for prod
```
docker-compose down ; docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```
#### multiple servers running in backend
```
docker-compose down ; docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```
### Check api status
Browse http://127.0.0.1/api/status

The following response should be shown:
```
{"status":"OK"}
```

### To get in the api container for dev / test
```
docker exec -it fastapi-crud-users-permission_api_1 /bin/bash
```

### To test everything
```
# Must be in the api container
pytest
```

## Documentation
Reminder: You should keep the container running
### Runnable doc
Browse http://127.0.0.1/api/docs

### Printable doc
Browse http://127.0.0.1/api/redoc

## Clean up

### Stop the instance
```
# remove-orphans for removing removed services in docker-compose.yml
docker-compose down --remove-orphans
# or
ctrl+C
```

### Remove all <none> image
```
docker rmi $(docker images -f “dangling=true” -q)
```

# Frontend (Only 10% done)
## Reminder: Still in development, did not take security into concern, don't use it directly.
Using [amis](https://github.com/baidu/amis) ([doc](https://baidu.github.io/amis)) to minimize the effort and knowledge needed. (80% setup could be done by json)

## Setup
Uncomment the frontend service in docker-compose, then just follow the setup in API part

### Check status
Browse http://127.0.0.1/status

## Try it
Browse http://127.0.0.1/login

## To do
* Page routing
* Authorization
* Application structure

## Archive

### For testing automation, not yet configured
```
docker-compose rm -f
docker-compose pull
docker-compose up --build -d
# Run some tests
./tests
docker-compose stop -t 1
```