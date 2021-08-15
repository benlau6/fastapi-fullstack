# fastapi-fullstack

## Introduction

A FastAPI project template with CRUD, authentication, authorization, documentation, testing, and frontend.

[Documentation](https://benlau6.github.io/fastapi-fullstack)

## Features

- [X] User system
- [X] Authorization per user, per row, per route
- [X] JWT authentication
- [X] Automatic OpenAPI documentation
- [X] Test automation
- [X] Type checking
- [X] Vue frontend

## Thanks to

- [fastapi](https://github.com/tiangolo/fastapi) ([doc](https://fastapi.tiangolo.com/)) for one of the best api framework in python. Don't skip the doc if you just knew it. It is perfectly written.
- [fastapi-permission](https://github.com/holgi/fastapi-permissions) ([doc](https://github.com/holgi/fastapi-permissions/blob/master/README.md)) for row-based security control.
- [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin) ([doc](https://panjiachen.github.io/vue-element-admin-site/)) ([demo](https://panjiachen.github.io/vue-element-admin))
- [traefik](https://github.com/traefik/traefik) ([doc](https://doc.traefik.io/traefik/)) for reverse proxy and payload size limiting.
- [pymongo](https://github.com/mongodb/mongo-python-driver) ([doc](https://pymongo.readthedocs.io/en/stable/tutorial.html)) for connecting MongoDB
- [pytest](https://github.com/pytest-dev/pytest) ([doc](https://docs.pytest.org/)) for testing
- [pydantic](https://github.com/samuelcolvin/pydantic/) ([doc](https://pydantic-docs.helpmanual.io/)) for data validation
- [pycodestyle](https://github.com/PyCQA/pycodestyle) for python style checking
- [black](https://github.com/psf/black) for automatic PEP8 formatting
- [mypy](https://github.com/python/mypy) ([doc](https://mypy.readthedocs.io/en/stable/)) for type checking


<small>

You may also wanna check [fastapi-pynamodb-lambda-simple](https://github.com/benlau6/fastapi-pynamodb-lambda-simple.git) or [fastapi-pynamodb-lambda-versioning](https://github.com/benlau6/fastapi-pynamodb-lambda-versioning) for using FastAPI on AWS

</small>

## Installation

``` bash
git clone https://github.com/benlau6/fastapi-fullstack.git
cd fastapi-fullstack
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

## Play it

- Backend: Browse <http://127.0.0.1/api/docs>
- Frontend: Browse <http://127.0.0.1>

## Reference

- Authentication
    - [jwt auth](https://segmentfault.com/a/1190000023185139)
- Nginx
    - [Is Nginx used and working?](https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/401)
    - [构建发布docker](https://github.com/PanJiaChen/vue-element-admin/issues/592)
    - [如何使用 docker 部署前端项目](https://shanyue.tech/frontend-engineering/docker.html)
- Cookie
    - [What is cookie?](https://shubo.io/cookies/)
- Tutorial
    - [hands on experience in vue-admin](https://juejin.cn/post/6844903840626507784)
    - [conclusion in vue-element-admin](https://www.gushiciku.cn/pl/pw8i/zh-tw)
- Project structure
    - [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/frontend)
    - [dispatch](https://github.com/Netflix/dispatch)
- Docker-compose
    - [overriding](https://docs.docker.com/compose/extends/#adding-and-overriding-configuration)

## License

This project is licensed under the terms of the MIT license.
