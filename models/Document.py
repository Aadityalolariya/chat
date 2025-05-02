from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_path = Column(String(150))
    document_type_id = Column(Integer, ForeignKey("constant.id")) # for future use, currently setting as null
    document_size = Column(Integer)
    created_on = Column(TIMESTAMP, default=datetime.utcnow)

