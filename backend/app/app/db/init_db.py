from typing import Any
from app import crud, schemas
from app.core.config import settings


def init_db(collection: Any) -> None:
    user = crud.user.get_by_email(collection, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(collection, document_in=user_in)  # noqa: F841
