from models.Message import Message
from schemas import MessageSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa


class MessageCrud(BaseCrud[Message, MessageSchema, MessageSchema]):
    pass


CRUDMessage = MessageCrud(Message)
