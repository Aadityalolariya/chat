from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chat.id"))
    content = Column(Text)
    message_timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("user.id"))
    message_type_id = Column(Integer, ForeignKey("constant.id"))
    status_id = Column(Integer, ForeignKey("constant.id"))
    document_id = Column(Integer, ForeignKey("document.id"))
    thread_id = Column(Integer, ForeignKey("thread.id"))
    reference_message_id = Column(Integer, ForeignKey("message.id"))

