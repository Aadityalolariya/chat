from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text, Boolean
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_name = Column(String(50))
    admin_user_id = Column(Integer, ForeignKey("user.id"))
    is_group_chat = Column(Boolean, nullable=False, default=False)
    created_on = Column(TIMESTAMP, default=datetime.utcnow)
