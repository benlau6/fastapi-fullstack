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
#### build the images
```
# it must be rerun if dockerfile / docker-compose.yml is changed
docker-compose build
```
#### single server for dev/test (server auto restart after py code change)
```
docker-compose up
```
#### multiple servers for prod
```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```
#### run in backend
```
docker-compose up -d
```
#### shortcut for develpment
```
docker-compose down; docker-compose up --build
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

#

# Frontend (Only 10% done)
Using [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin) ([doc](https://panjiachen.github.io/vue-element-admin-site/)) ([preview](https://panjiachen.github.io/vue-element-admin))

## Setup
Keep the containers running, then run codes below:
```
# git pull https://github.com/benlau6/fastapi-crud-users-permission.git
# cd fastapi-crud-users-permission
cd frontend
npm install
npm run dev
```

### Try it
Browse http://127.0.0.1:9528/

## To do
* [ ] connect to all the endpoints
* [ ] make some demos

## Q&A
1. Q: set-cookies not working? 

A1: src/utils/auth.js -> set **const TokenKey = 'fastapiusersauth'**

A2: src/utils/requests.js -> axios set **withCredentials: true**
```
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})
```

A3: (fastapi) api/fastapi_users_utils.py -> set **CookieAuthentication(..., cookie_samesite='None')**



2. Q: jwt auth not working? \

A. src/utils/requests.js -> request interceptor set **config.headers['Authorization'] = 'Bearer ' + getToken()**
```
service.interceptors.request.use(
...
    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['Authorization'] = 'Bearer ' + getToken()
    }
    return config
  },
...
```

3. Q: Backend response format not matching?

A. src/utils/requests.js -> response interceptor set **const res = {...}**
```
service.interceptors.response.use(
...
  response => {
    const hasData = response.data != null
    const hasDetail = hasData ? response.data.detail != null : false
    const res = {
      'code': response.status,
      'data': hasData ? response.data : null,
      'message': hasDetail ? response.data.detail : null
    }
...
```

A.alt (fastapi) app/main.py -> add middleware to handle response
```
# it formatted response, but openapi crashed
import json
class async_iterator_wrapper:
    def __init__(self, obj):
        self._it = iter(obj)
    def __aiter__(self):
        return self
    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


@app.middleware("http")
async def format_output_for_frontend(request: Request, call_next):
    response = await call_next(request)
    
    res_body = [x async for x in response.__dict__['body_iterator']]
    
    try:
        if 200 <= response.status_code < 300:
            status = True
        else:
            status = False

        res_body_json = res_body[0]
        res_body_data = json.loads(res_body_json)
        if res_body_data is not None:
            msg = res_body_data.pop('detail', None)
            data = dict(res_body_data)
        else:
            msg = None
            data = None

        res_body_data = {
            'status': status,
            'msg': msg,
            'data': data,
        }
        res_body_json = json.dumps(res_body_data)
        res_body = [res_body_json.encode()]
        response.headers['content-length'] = str(len(res_body_json))
    except:
        pass
    
    response.__setattr__('body_iterator', async_iterator_wrapper(res_body))
    
    return response
```

4. Q: permission not stated as 'roles' in response body?

A. ctrl+f to find 'roles', replace some of them carefully



## Reference
1. Authentication
  1. [jwt auth](https://segmentfault.com/a/1190000023185139)
2. Nginx
  1. [Is Nginx used and working?](https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/401)
3. Cookie
  1. [What is cookie?](https://shubo.io/cookies/)
4. Tutorial
  1. [hands on experience in vue-admin](https://juejin.cn/post/6844903840626507784)
  2. [conclusion in vue-element-admin](https://www.gushiciku.cn/pl/pw8i/zh-tw)

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