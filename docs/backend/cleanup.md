# Cleanup

## Stop the instance

++ctrl+c++ 

or

``` bash
docker-compose down
```



## Remove unused services

``` bash
docker-compose down --remove-orphans
```

## Remove all <none\> images

``` bash
docker rmi $(docker images -f “dangling=true” -q)
```