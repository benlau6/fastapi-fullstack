from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from bson.objectid import ObjectId

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


DBModelType = TypeVar("DBModelType", bound=dict)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[DBModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, db_schema):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.db_schema = db_schema


    def get(self, collection, id: Union[str, ObjectId]) -> Optional[DBModelType]:
        if isinstance(id, str):
            id = ObjectId(id)
        return collection.find_one({'_id': id})

    def get_multi(
        self, collection, *, skip: int = 0, limit: int = 100
    ) -> List[DBModelType]:
        return list(collection.find().skip(skip).limit(limit))

    def create(self, collection, *, document_in: CreateSchemaType) -> DBModelType:
        document_to_db= self.db_schema(**document_in.dict())
        document_to_db_data = document_to_db.dict()
        document_id = collection.insert_one(document_to_db_data).inserted_id
        document_to_db_data['_id'] = document_id
        return document_to_db_data

    # exclude_unset=True is to exclude default values, very useful for partial update
    # password or hashed_password is not excluded 
    # because it is in document_in, which will be passed until the end
    def update(
        self,
        collection,
        *,
        db_document: DBModelType,
        document_in: UpdateSchemaType
    ) -> DBModelType:
        document_to_db= self.db_schema(**document_in.dict(exclude_unset=True))
        document_to_db_data = document_to_db.dict(exclude_unset=True)
        result = collection.update_one(db_document, {'$set': document_to_db_data})
        return result.matched_count, result.modified_count

    def delete(self, collection, *, id: Union[str, ObjectId]) -> DBModelType:
        if isinstance(id, str):
            id = ObjectId(id)
        result = collection.delete_one({'_id': id})
        return result.deleted_count