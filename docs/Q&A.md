# Q&A

!!! question "Set-cookies not working?"
??? solution
    === "Solution 1"
        src/utils/auth.js -> set **const TokenKey = 'fastapiusersauth'**
    === "Solution 2"
        1. (fastapi) api/fastapi_users_utils.py -> set **CookieAuthentication(..., cookie_samesite='None')**
        2. src/utils/requests.js -> axios set **withCredentials: true** 
        ``` python
        const service = axios.create({
        baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
        withCredentials: true, // send cookies when cross-domain requests
        timeout: 5000 // request timeout
        })
        ```
!!! question "JWT auth not working?"
??? solution
    src/utils/requests.js -> request interceptor set **config.headers['Authorization'] = 'Bearer ' + getToken()**
    ``` python
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
!!! question "Backend response format not matching?"
??? solution
    === "Solution 1"
        src/utils/requests.js -> response interceptor set **const res = {...}** 
        ``` python
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
    === "Solution 2"
        (fastapi) app/main.py -> add middleware to handle response
        ``` python
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
!!! question "Permission not stated as 'roles' in response body?"
??? solution
    ++ctrl+f++ to find 'roles', replace some of them carefully
!!! question "app/prestart.sh not found?"
??? solution
    set **git config core.autocrlf false** before using 'git add .' if you are using windows