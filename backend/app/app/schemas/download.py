from datetime import datetime
from typing import Any, Tuple, List

from pydantic import BaseModel
from fastapi import Form
from fastapi_permissions import Allow, Authenticated, All


class DownloadQuery(BaseModel):
    project: str = Form(...)
    dataset: str = Form(...)
    year: int = Form(..., ge=2000, le=datetime.now().year + 1)
    month: int = Form(..., ge=1, le=12)
    day: int = Form(..., ge=1, le=31)

    def __acl__(self) -> List[Tuple[Any, str, Any]]:
        return [
            (Allow, "role:admin", All),
            (Allow, f"download:{self.project}:all", "submit"),
            (Allow, f"download:{self.project}:{self.dataset}", "submit"),
        ]

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
