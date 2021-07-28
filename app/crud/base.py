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
        document_in_db_schema= self.db_schema(**document_in.dict())
        document_in_data = document_in_db_schema.dict()
        document_id = collection.insert_one(document_in_data).inserted_id
        document_in_data['_id'] = document_id
        return document_in_data

    def update(
        self,
        collection,
        *,
        db_document: DBModelType,
        document_in: UpdateSchemaType
    ) -> DBModelType:
        document_in_db_schema= self.db_schema(**document_in.dict(exclude_unset=True))
        document_in_data = document_in_db_schema.dict(exclude_unset=True)
        result = collection.update_one(db_document, {'$set': document_in_data})
        return result.matched_count, result.modified_count

    def delete(self, collection, *, db_document: DBModelType) -> DBModelType:
        result = collection.delete_one(db_document)
        return result.deleted_count