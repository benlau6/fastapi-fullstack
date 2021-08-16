from pydantic import BaseModel


class UpdateResponse(BaseModel):
    matched_count: int
    modified_count: int


class DeleteResponse(BaseModel):
    deleted_count: int
