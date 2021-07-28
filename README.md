# fastapi-mongo-oauth

## Setup

### To build all the containers with log shown
```
git pull https://github.com/benlau6/fastapi-mongo-oauth.git
docker-compose up --build
```

### Check api status
browse http://api.docker.localhost/api/status with response
```
{"status":"OK"}
```

### To get in the api container for dev / test
```
docker exec -it fastapi-mongo-oauth_api_1 /bin/bash
```

### To test everything
```
pytest
```

## Documentation
### Runnable doc
Goto 127.0.0.1/docs

### Printable doc
Goto 127.0.0.1/redoc


## Clean up

### Stop the instance
```
docker-compose down
# or
Ctrl+C
```
### Remove all <none> image
```
docker rmi $(docker images -f “dangling=true” -q)
```

## Archive

### To build all the containers, test, and shut all down
```
docker-compose rm -f
docker-compose pull
docker-compose up --build -d
# Run some tests
./tests
docker-compose stop -t 1
```