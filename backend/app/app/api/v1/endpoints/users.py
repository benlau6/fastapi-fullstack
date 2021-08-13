from typing import Any, List, Dict, Optional, Tuple

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from bson import ObjectId

from app import crud, schemas
from app.api import deps
from app.core.config import settings


router = APIRouter()


@router.get("/", response_model=List[schemas.UserFromDB])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.UserInDB = Depends(deps.get_current_active_superuser),
    collection: Any = Depends(deps.get_user_collection),
) -> List[schemas.UserInDB]:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(collection, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.UserFromDB)
def create_user(
    *,
    user_in: schemas.UserCreate,
    current_user: schemas.UserInDB = Depends(deps.get_current_active_superuser),
    collection: Any = Depends(deps.get_user_collection),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(collection, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(collection, document_in=user_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #    send_new_account_email(
    #        email_to=user_in.email, username=user_in.email, password=user_in.password
    #    )
    return user


@router.put("/me", response_model=schemas.UpdateResponse)
def update_user_me(
    *,
    password: str = Body(None),
    email: EmailStr = Body(None),
    current_user: schemas.UserInDB = Depends(deps.get_current_active_user),
    collection: Any = Depends(deps.get_user_collection),
) -> Tuple[int, int]:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    user = crud.user.update(collection, id=current_user["_id"], document_in=user_in)
    return user


@router.get("/me", response_model=schemas.UserFromDB)
def read_user_me(
    current_user: schemas.UserInDB = Depends(deps.get_current_active_user),
) -> schemas.UserInDB:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.UserFromDB)
def create_user_open(
    *,
    email: EmailStr = Body(...),
    password: str = Body(...),
    collection: Any = Depends(deps.get_user_collection),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(collection, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email)
    user = crud.user.create(collection, document_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.UserFromDB)
def read_user_by_id(
    user_id: str,
    current_user: schemas.UserInDB = Depends(deps.get_current_active_user),
    collection: Any = Depends(deps.get_user_collection),
) -> Optional[schemas.UserInDB]:
    """
    Get a specific user by id.
    """
    user = crud.user.get(collection, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.UpdateResponse)
def update_user(
    *,
    user_id: str,
    user_in: schemas.UserUpdate,
    current_user: schemas.UserInDB = Depends(deps.get_current_active_superuser),
    collection: Any = Depends(deps.get_user_collection),
) -> Dict[str, int]:
    """
    Update a user.
    """
    user = crud.user.get(collection, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exists",
        )
    if user_in.email is not None:
        check_user = crud.user.get_by_email(collection, email=user_in.email)
        if check_user is not None:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
    matched_count, modified_count = crud.user.update(
        collection, id=user_id, document_in=user_in
    )
    return {"matched_count": matched_count, "modified_count": modified_count}


@router.delete("/{user_id}", response_model=schemas.DeleteResponse)
def delete_user(
    *,
    user_id: str,
    current_user: schemas.UserInDB = Depends(deps.get_current_active_superuser),
    collection: Any = Depends(deps.get_user_collection),
) -> Dict[str, int]:
    """
    Delete a user.
    """
    deleted_count = crud.user.delete(collection, id=user_id)
    return {"deleted_count": deleted_count}
