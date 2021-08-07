# fastapi-fullstack

## FastAPI backend

### Setup

Reminder: All project development, testing, and deployment are done in windows10/11. docker-compose\*.yml may need to be changed for linux/mac environment

#### To build and run the container

##### Get to the workdir

```bash
git pull https://github.com/benlau6/fastapi-fullstack.git
cd fastapi-fullstack
```
##### Build the images

```
# it must be rerun if dockerfile / docker-compose.yml is changed (e.g. dev -> prod, code changes)
docker-compose build
# or
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

```
##### Load built images for offline production

```bash
# docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker save -o fastapi-fullstack.tar fastapi-fullstack_api fastapi-fullstack_frontend traefik
# send the .tar to offline server
docker load -i fastapi-fullstack.tar
```

##### Single server for dev/test (server auto restart after py code change)

```bash
docker-compose up
```

##### Multiple servers for prod

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

##### Run in backend

```bash
docker-compose up -d
```

##### Shortcut for develpment

```bash
docker-compose down; docker-compose up --build
```

#### Check api status

Browse http://127.0.0.1/api/status

The following response should be shown:
```bash
{"status":"OK"}
```

#### To get in the api container for dev / test

```bash
docker exec -it fastapi-fullstack_api_1 /bin/bash
```

#### To test everything

```bash
# docker exec -it fastapi-fullstack_api_1 /bin/bash
pytest
```

### Documentation

Reminder: You should keep the container running

#### Runnable doc

Browse http://127.0.0.1/api/docs

#### Printable doc

Browse http://127.0.0.1/api/redoc

### Clean up

#### Stop the instance

```bash
# remove-orphans for removing removed services in docker-compose.yml
docker-compose down --remove-orphans
# or
ctrl+C
```

#### Remove all <none> image

```bash
docker rmi $(docker images -f “dangling=true” -q)
```

## vue-element-admin Frontend (only 30% done)

### To do

- [ ] connect to all the endpoints
- [ ] make some demos

### Setup

#### dev

Keep the containers running, then run codes below:
```bash
# git pull https://github.com/benlau6/fastapi-fullstack.git
# cd fastapi-fullstack
# docker-compose up --build
cd frontend/app
npm install
npm run dev
```
#### prod

Check setup for backend

#### Try it

Browse http://127.0.0.1:9528 for dev

Browse http://127.0.0.1 for prod

### Q&A

- Set-cookies not working?
  - Solultion 1: src/utils/auth.js -> set **const TokenKey = 'fastapiusersauth'**
  - Solution 2:
    - step 1: (fastapi) api/fastapi_users_utils.py -> set **CookieAuthentication(..., cookie_samesite='None')**
    - step 2: src/utils/requests.js -> axios set **withCredentials: true** 
      ```
      const service = axios.create({
        baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
        withCredentials: true, // send cookies when cross-domain requests
        timeout: 5000 // request timeout
      })
      ```
- JWT auth not working?
  - src/utils/requests.js -> request interceptor set **config.headers['Authorization'] = 'Bearer ' + getToken()**
    ```python
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
- Backend response format not matching?
  - Solution 1: src/utils/requests.js -> response interceptor set **const res = {...}** 
    ```python
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
  - Solution 2: (fastapi) app/main.py -> add middleware to handle response
    ```python
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
- Permission not stated as 'roles' in response body?
  - ctrl+f to find 'roles', replace some of them carefully
- app/prestart.sh not found?
  - set **git config core.autocrlf false** before using 'git add .' if you are using windows

## Archive

For testing automation, not yet configured
```bash
docker-compose rm -f
docker-compose pull
docker-compose up --build -d
# Run some tests
./tests
docker-compose stop -t 1
```