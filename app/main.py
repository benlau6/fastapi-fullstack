from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app import models, crud
from app.core.config import settings
from app.api.fastapi_users_utils import fastapi_users
from app.api.v1.api import router as api_v1_router



app = FastAPI(root_path=settings.ROOT_STR)
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]}, # 
    generate_schemas=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.on_event('startup')
async def create_first_super_user():
    user = await crud.user.get_by_email(db=None, email=settings.FIRST_SUPERUSER)
    if user is None:
        await fastapi_users.create_user(
            models.UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
        )


@app.get("/status")
def read_api_status():
    return {"status": "OK"}
