from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from db import Base
from datetime import datetime


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chat.id"))
    content = Column(Text)
    sender_id = Column(Integer, ForeignKey("user.id"))
    document_id = Column(Integer, ForeignKey("document.id"))
    parent_message_id = Column(Integer, ForeignKey("message.id"), index=True)
    reference_message_id = Column(Integer, ForeignKey("message.id"))
    created_on = Column(TIMESTAMP, default=datetime.utcnow)


