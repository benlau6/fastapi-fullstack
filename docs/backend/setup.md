# Setup


!!! note
    All project development, testing, and deployment are done in windows10/11. docker-compose\*.yml may need to be changed for linux/mac environment

## To build and run the container

### Get to the workdir

``` bash
git pull https://github.com/benlau6/fastapi-fullstack.git
cd fastapi-fullstack
```

### Build the images

```
# it must be rerun if dockerfile / docker-compose.yml is changed (e.g. dev -> prod, code changes)
docker-compose build
# or
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

```
### Load built images for offline production

``` bash
# docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker save -o fastapi-fullstack.tar fastapi-fullstack_api fastapi-fullstack_frontend traefik
# send the .tar to offline server
docker load -i fastapi-fullstack.tar
```

### Single server for dev/test (server auto restart after py code change)

``` bash
docker-compose up
```

### Multiple servers for prod

``` bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Run in backend

``` bash
docker-compose up -d
```

### Shortcut for develpment

``` bash
docker-compose down; docker-compose up --build
```

## Check api status

Browse http://127.0.0.1/api/status

The following response should be shown:
``` bash
{"status":"OK"}
```

## To get in the api container for dev / test

``` bash
docker exec -it fastapi-fullstack_api_1 /bin/bash
```

## To test everything

``` bash
# docker exec -it fastapi-fullstack_api_1 /bin/bash
pytest
```

## Stop the instance

``` bash
# remove-orphans for removing removed services in docker-compose.yml
docker-compose down --remove-orphans
# or
ctrl+C
```

## Remove all <none> image

``` bash
docker rmi $(docker images -f “dangling=true” -q)
```