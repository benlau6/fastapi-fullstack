from pydantic import BaseModel


class Potato(BaseModel):
    id: int
    color: str
    mass: float
