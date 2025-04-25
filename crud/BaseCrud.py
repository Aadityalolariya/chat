from typing import Type, TypeVar, Generic, Union, Dict
from sqlalchemy.orm import Session
import sqlalchemy as sa
from pydantic import BaseModel
from db import Base  # SQLAlchemy Base model

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, SchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model  # To be defined in subclasses

    def create(self, db: Session, obj_in: SchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())  # `BaseCrud.model` will be set in subclasses
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, id: int) -> ModelType | None:
        return db.query(self.model).filter(BaseCrud.model.id == id).first()

    def get_all(self, db: Session, limit: int = 1000):
        return db.query(self.model).limit(limit).all()

    def update(self, db: Session, obj_id: int, obj_in: Dict) -> ModelType:
        query = sa.update(self.model).filter(self.model.id == obj_id).values(**obj_in)
        db.execute(query)
        db.flush()
        return True

    def delete(self, db: Session, id: int) -> bool:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.flush()
            return True
        return False
