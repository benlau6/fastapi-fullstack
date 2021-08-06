from tortoise import Tortoise

from app import models, schemas
from app.core.config import settings
from app.api.fastapi_users_utils import fastapi_users_instance


async def init_db() -> None:
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

    admin_email = settings.FIRST_SUPERUSER
    found_users = await models.UserModel.filter(email=admin_email).count()
    
    if found_users == 0:
        obj_in = schemas.UserCreate(
            email=admin_email,
            password='password',
            is_superuser=True,
            is_verified=True,
            principals=['role:admin', 'user:'+admin_email]
        )
        await fastapi_users_instance.create_user(obj_in)
    
    await Tortoise.close_connections()