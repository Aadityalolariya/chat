from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Reaction(Base):
    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("message.id"))
    content = Column(String(90))
    reacted_by_id = Column(Integer, ForeignKey("user.id"))
    reacted_on = Column(TIMESTAMP, default=datetime.utcnow)
