from typing import Any, Optional, List, Tuple
from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr
from fastapi import Form
from fastapi_permissions import Allow, Authenticated, All

from app.schemas.utils import as_form


class UploadRecord(BaseModel):
    filename: str
    file_size: Optional[str] = None
    file_content_type: str
    created_by: datetime = datetime.now().astimezone()
    updated_by: datetime = datetime.now().astimezone()
    owner: EmailStr

    @property
    def created_by_hkt(self) -> datetime:
        return self.created_by + timedelta(hours=8)

    @property
    def updated_by_hkt(self) -> datetime:
        return self.updated_by + timedelta(hours=8)


@as_form
class UploadForm(BaseModel):
    project: str = Form(...)
    dataset: str = Form(...)
    year: int = Form(..., ge=2000)
    month: int = Form(..., ge=1, le=12)
    day: int = Form(..., ge=1, le=31)

    def __acl__(self) -> List[Tuple[Any, str, Any]]:
        return [
            (Allow, "role:admin", All),
            (Allow, f"upload:{self.project}:all", "submit"),
            (Allow, f"upload:{self.project}:{self.dataset}", "submit"),
        ]

    def as_form(self) -> None:
        # to be replaced by as_form decorator
        pass

    @property
    def date_padding_prefix(self) -> str:
        return f"/{self.year}/{self.month:02}/{self.day:02}"

    @property
    def date_prefix(self) -> str:
        return f"/{self.year}/{self.month}/{self.day}"

    @property
    def date_str(self) -> str:
        return f"{self.year}{self.month:02}{self.day:02}"

    @property
    def zip_filename(self) -> str:
        return f"{self.date_str}_{self.project}_{self.dataset}"

    @property
    def base_dir(self) -> str:
        return f"{self.project}/{self.dataset}{self.date_prefix}"


class UploadRecords(BaseModel):
    records: Optional[List[UploadRecord]] = None
