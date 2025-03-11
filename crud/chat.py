from models.Chat import Chat
from schemas import ChatSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa


class ChatCrud(BaseCrud[Chat, ChatSchema, ChatSchema]):
    pass


CRUDChat = ChatCrud(Chat)
