from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text, Boolean, JSON
from db import Base
from datetime import datetime


class MessageSeenStatus(Base):
    __tablename__ = "message_seen_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("message.id"))
    seen_status = Column(Text, nullable=True)
