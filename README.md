# fastapi-fullstack

## Introduction
A FastAPI project template with CRUD, authentication, authorization, documentation, testing, and frontend.

[Documentation](https://benlau6.github.io/fastapi-fullstack)

### Features
- [X] Authentication with registration, login, password reset and email verification 
- [X] Authorization per user, per row, per route
- [X] ORM support
- [X] JWT and cookie authentication backends
- [X] Quick CRUD endpoints creation
- [X] Automatic OpenAPI documentation
- [X] Test Automation
- [X] Vue frontend

### Thanks to
- [fastapi](https://github.com/tiangolo/fastapi) ([doc](https://fastapi.tiangolo.com/)) for one of the best api framework in python. Don't skip the doc if you just knew it. It is perfectly written.
- [fastapi-users](https://github.com/frankie567/fastapi-users) ([doc](https://frankie567.github.io/fastapi-users/)) for comprehensive user model.
- [fastapi-permission](https://github.com/holgi/fastapi-permissions) ([doc](https://github.com/holgi/fastapi-permissions/blob/master/README.md)) for row-based security control.
- [fastapi-crudrouter](https://github.com/awtkns/fastapi-crudrouter) ([doc](https://fastapi-crudrouter.awtkns.com/)) for quick crud development.
- [tortoise-orm](https://github.com/tortoise/tortoise-orm) ([doc](https://tortoise-orm.readthedocs.io/en/latest/)) for database orm, you can switch to any other orms for new features without any problems. However, if you want to switch it for features in use, e.g. fastapi-users and fastapi-permission. Re-configuration of pytest is needed.
- [traefik](https://github.com/traefik/traefik) ([doc](https://doc.traefik.io/traefik/)) for reverse proxy and payload size limiting.
- [pytest](https://github.com/pytest-dev/pytest) ([doc](https://docs.pytest.org/)) for testing
- [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin) ([doc](https://panjiachen.github.io/vue-element-admin-site/)) ([demo](https://panjiachen.github.io/vue-element-admin))

### Notes
Some fastapi third party libraries are selected because they earned many stars, well developed and maintained. 
Many new features could be added in without any efforts. But most of the features you may use can acutally be rebuilt with only some efforts. 
So if for educational purpose, to know what had been done, or for full control in workflow, to set what should be done, I recommend to build from scratch with only FastAPI. 

You may want to check [fastapi-mongo-oauth](https://github.com/benlau6/fastapi-mongo-oauth), which is built from scratch with mongo.

You may also wanna check [fastapi-pynamodb-lambda-simple](https://github.com/benlau6/fastapi-pynamodb-lambda-simple.git) for using FastAPI on AWS \
(or [fastapi-pynamodb-lambda-versioning](https://github.com/benlau6/fastapi-pynamodb-lambda-versioning) for better project file structure)

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
