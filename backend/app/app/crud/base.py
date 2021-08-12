from typing import Generic, List, Optional, TypeVar, Union, Tuple, Dict
from bson.objectid import ObjectId

from pydantic import BaseModel


DBModelType = TypeVar("DBModelType", bound=Dict)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[DBModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, to_db_schema):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.to_db_schema = to_db_schema

    def get(self, collection, id: Union[str, ObjectId]) -> Optional[DBModelType]:
        if isinstance(id, str):
            id = ObjectId(id)
        return collection.find_one({"_id": id})

    def get_multi(
        self, collection, *, skip: int = 0, limit: int = 100
    ) -> List[DBModelType]:
        return list(collection.find().skip(skip).limit(limit))

    def create(self, collection, document_in: CreateSchemaType) -> ObjectId:
        document_to_db = self.to_db_schema(**document_in.dict())
        document_to_db_data = document_to_db.dict()
        return collection.insert_one(document_to_db_data).inserted_id

    def update(
        self, collection, id: Union[str, ObjectId], document_in: UpdateSchemaType
    ) -> Tuple[int, int]:
        if isinstance(id, str):
            id = ObjectId(id)
        # format document_in
        # exclude_unset=True is to exclude default values, very useful for partial update
        # password or hashed_password is not excluded
        # because it is in document_in, which will be passed until the end
        document_to_db = self.to_db_schema(**document_in.dict(exclude_unset=True))
        document_to_db_data = document_to_db.dict(exclude_unset=True)
        # update by id
        result = collection.update_one({"_id": id}, {"$set": document_to_db_data})
        return result.matched_count, result.modified_count

    def delete(self, collection, id: Union[str, ObjectId]) -> int:
        if isinstance(id, str):
            id = ObjectId(id)
        result = collection.delete_one({"_id": id})
        return result.deleted_count
