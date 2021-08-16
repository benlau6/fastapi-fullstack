# Q&A

!!! question "JWT auth not working?"
??? solution
    (frontend) app/src/utils/requests.js -> request interceptor set **config.headers['Authorization'] = 'Bearer ' + getToken()**
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
        (backend) Change your response_model schemas in app/app/api/schemas
    === "Solution 2"
        (frontend) app/src/utils/requests.js -> response interceptor set **const res = {...}** 
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
    === "Solution 3"
        (backend) app/app/main.py -> add middleware to handle response
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
            response = call_next(request)
            
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

!!! question "Cookie is not stored?"
??? solution
    === "Solution 1 - cookie size"
        (backend) Ensure cookie body is not larger than 4kb, otherwise use sessionStorage instead at app/src/utils/auth.js
         ``` javascript
         export function getToken() {
         return sessionStorage.getItem(TokenKey)
         }

         export function setToken(token) {
         return sessionStorage.setItem(TokenKey, token)
         }

         export function removeToken() {
         return sessionStorage.removeItem(TokenKey)
         }
         ```
    === "Solution 2 - with reverse proxy"
        Check your host, port configs in traefik, frontend, backend
    === "Solution 3 - without reverse proxy"
        1. (backend) Enable CORSMiddleware at app/app/main.py
            ``` python
            # to enable Access-Control-Allow-Credentials
            # to enable Access-Control-Allow-Origin for frontend origin
            # P.S. Origin is only considered to be the same if the protocol, host and port is the same
            # Ref. https://www.w3.org/Security/wiki/Same_Origin_Policy
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[
                    'http://localhost:9528',
                    'http://127.0.0.1:9528'
                    ],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            ```
        2. (frontend) Enable axios withCredentials at app/src/utils/request.js
            ``` javascript
            const service = axios.create({
                baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
                withCredentials: true, // send cookies when cross-domain requests
                timeout: 5000 // request timeout
                })
            ```
    === "Solution 4 - using fastapi-users"
        1. (frontend) app/src/utils/auth.js -> set **const TokenKey = 'fastapiusersauth'**
        2. (fastapi-users) set **CookieAuthentication(..., cookie_samesite='None')**