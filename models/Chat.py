from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_type_id = Column(Integer, ForeignKey("constant.id"))
    chat_name = Column(String(50))
    admin_user_id = Column(Integer, ForeignKey("user.id"))
    created_on = Column(TIMESTAMP, default=datetime.utcnow)
