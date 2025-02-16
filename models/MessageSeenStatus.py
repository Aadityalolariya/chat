from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class MessageSeenStatus(Base):
    __tablename__ = "message_seen_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("message.id"))
    sent_status_id = Column(Integer, ForeignKey("constant.id"))
