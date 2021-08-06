from fastapi import Form
from pydantic import BaseModel
from typing import Type
from app.core.config import settings
import inspect


def as_form(cls: Type[BaseModel]):
    new_params = []
    for field in cls.__fields__.values():
        new_params.append(
            inspect.Parameter(
                field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                annotation=cls.__annotations__[field.name],
                default=(
                    Form(
                        field.default if not field.required else ...,
                        alias=field.alias,
                        description=getattr(field.field_info, 'description', None),
                        ge=getattr(field.field_info, 'ge', None),
                        gt=getattr(field.field_info, 'gt', None),
                        le=getattr(field.field_info, 'le', None),
                        lt=getattr(field.field_info, 'lt', None),
                        max_length=getattr(field.field_info, 'max_length', None),
                        min_length=getattr(field.field_info, 'min_length', None),
                        regex=getattr(field.field_info, 'regex', None),
                        title=getattr(field.field_info, 'title', None),
                        media_type=getattr(field.field_info, 'media_type', None),
                        **field.field_info.extra,
                    )
                ),
            )
        )

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, 'as_form', _as_form)

    return cls
