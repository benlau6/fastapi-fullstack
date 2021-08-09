# Deployment

!!! note
    All project development, testing, and deployment are done in windows10/11. docker-compose\*.yml may need to be changed for linux/mac environment

!!! note
    Docker should be installed

## Pull the repository

``` bash
git pull https://github.com/benlau6/fastapi-fullstack.git
cd fastapi-fullstack
```

## Build the images

``` bash
# it must be rerun if dockerfile / docker-compose.yml is changed 
# e.g. dev -> prod, code changes
docker-compose build
# or
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
```

!!! notes "Offline steps (Optional)"
    1. Save the built images to .tar

        ``` bash
        docker save -o fastapi-fullstack.tar fastapi-fullstack_api fastapi-fullstack_frontendtraefik
        ```

    2. Send the .tar to the offline server

        ``` bash
        docker load -i fastapi-fullstack.tar
        ```

## Dev/test stage

- Single server
- Apply code changes automatically

``` bash
docker-compose up
```

## Prod stage

- Multiple servers

``` bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Check api status

Browse http://127.0.0.1/api/status

The following response should be shown:
``` bash
{"status":"OK"}
```

## Optional commands

!!! note "Run servers in backend"
    ``` bash
    docker-compose up -d
    ```

!!! note "Shortcut for develpment steps"
    ``` bash
    docker-compose down; docker-compose up --build
    ```