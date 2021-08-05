from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app import schemas, models
from app.core.config import settings
from app.api.v1.api import router as api_v1_router
from app.api.fastapi_users_utils import fastapi_users_instance


def create_app() -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_STR)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost:8000',
            'http://localhost:3000',
            'http://localhost:9528'
            ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix=settings.API_V1_STR)


    @app.get("/status")
    def read_api_status():
        return {"status": "OK"}

    return app

app = create_app()

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
)


# just for dev
@app.on_event('startup')
async def startup() -> None:
    # init_first_super_user
    email = settings.FIRST_SUPERUSER
    found_users = await models.UserModel.filter(email=email).count()
    if found_users < 1:
        obj_in = schemas.UserCreate(
            email=email,
            password='password',
            is_superuser=True,
            is_verified=True,
            principals=['role:admin', 'user:'+email]
        )
        await fastapi_users_instance.create_user(obj_in)


@app.on_event('shutdown')
async def shutdown() -> None:
    pass
