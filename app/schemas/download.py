from pydantic import BaseModel
from fastapi import Form
from app.schemas.utils import as_form
from datetime import datetime
from app.core.config import settings


@as_form
class DownloadForm(BaseModel):
    project: str = Form(...)
    dataset: str = Form(...)
    year: int = Form(..., ge=2000, le=datetime.now().year+1)
    month: int = Form(..., ge=1, le=12)
    day: int = Form(..., ge=1, le=31)

    @property
    def date_padding_prefix(self):
        return f'/{self.year}/{self.month:02}/{self.day:02}'

    @property
    def date_prefix(self):
        return f'/{self.year}/{self.month}/{self.day}'        

    @property
    def date_str(self):
        return f'{self.year}{self.month:02}{self.day:02}'

    @property
    def zip_filename(self):
        return f'{self.date_str}_{self.project}_{self.dataset}'

    @property
    def base_dir(self):
        return f'{self.project}/{self.dataset}{self.date_prefix}'    

