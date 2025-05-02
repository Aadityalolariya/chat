from sqlalchemy import Column, Integer, ForeignKey
from db import Base


class UnseenMessages(Base):
    __tablename__ = "unseen_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("message.id"))
    chat_id = Column(Integer, ForeignKey("chat.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
