from uuid import UUID, uuid4
from typing import Optional, List 
from datetime import datetime, time, timedelta
from pydantic import BaseModel


class DownloadBase(BaseModel):
    database: str
    table: str
    q: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class DownloadIn(DownloadBase):
    id: UUID = uuid4()
    api_key: str
    source: str = 'api'


class DownloadOut(DownloadBase):
    pass


class DownloadOutList(BaseModel):
    api_key: str
    data: List[DownloadOut]
