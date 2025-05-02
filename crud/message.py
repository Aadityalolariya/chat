from models.Message import Message
from schemas import MessageSchema
from crud import BaseCrud


class MessageCrud(BaseCrud[Message, MessageSchema, MessageSchema]):
    pass


CRUDMessage = MessageCrud(Message)
