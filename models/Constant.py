from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Constant(Base):
    __tablename__ = "constant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("group.id"))
    code = Column(String(50), unique=True, nullable=False)

