from typing import Any, Dict, Generator, Type, List, Union, Protocol
import inspect
import re

from fastapi import Form
from pydantic import BaseModel, constr
from bson.objectid import ObjectId

from typing import Protocol, TypeVar, Callable, Optional, cast


# https://github.com/python/mypy/issues/2087
# to fix Callable has no attribute "signature"
# Note: can use a more restrictive bound if wanted.
F = TypeVar("F", bound=Callable[..., object])


class ActionWithAttributes(Protocol[F]):
    __signature__: Optional[inspect.Signature]
    __call__: F


def action_with_attributes(action: F) -> ActionWithAttributes[F]:
    action_with_attributes = cast(ActionWithAttributes[F], action)
    # Make sure the cast isn't a lie.
    action_with_attributes.__signature__ = None
    return action_with_attributes


def as_form(cls: Type[BaseModel]) -> Type[BaseModel]:
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
                        description=getattr(field.field_info, "description", None),
                        ge=getattr(field.field_info, "ge", None),
                        gt=getattr(field.field_info, "gt", None),
                        le=getattr(field.field_info, "le", None),
                        lt=getattr(field.field_info, "lt", None),
                        max_length=getattr(field.field_info, "max_length", None),
                        min_length=getattr(field.field_info, "min_length", None),
                        regex=getattr(field.field_info, "regex", None),
                        title=getattr(field.field_info, "title", None),
                        media_type=getattr(field.field_info, "media_type", None),
                        **field.field_info.extra,
                    )
                ),
            )
        )

    @action_with_attributes
    async def _as_form(**data: Dict[str, Any]) -> BaseModel:
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)

    return cls


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, ObjectId]) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string")


# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
scope_regex = re.compile(r"^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$")


class Scope(str):
    
    @classmethod
    def __get_validators__(cls) -> Generator:
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # some example scopes
            examples=["role:admin", "upload:project:dataset"],
        )

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("string required")
        m = scope_regex.fullmatch(v.lower())
        if not m:
            raise ValueError("invalid scope format")
        # you could also return a string here which would mean model.scope
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(m.group(0))

    def __repr__(self) -> str:
        return f"Scope({super().__repr__()})"
