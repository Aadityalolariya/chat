from models.ChatUserMap import ChatUserMap
from schemas import ChatUserMapSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa


class ChatUserMapCrud(BaseCrud[ChatUserMap, ChatUserMapSchema, ChatUserMapSchema]):
    pass


CRUDChatUserMap = ChatUserMapCrud(ChatUserMap)
