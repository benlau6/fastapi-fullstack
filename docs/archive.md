# Archive

For testing automation, not yet configured
``` bash
docker-compose rm -f
docker-compose pull
docker-compose up --build -d
# Run some tests
./tests
docker-compose stop -t 1
```