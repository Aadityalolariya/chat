from models.ChatUserMap import ChatUserMap
from schemas import ChatUserMapSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder


class ChatUserMapCrud(BaseCrud[ChatUserMap, ChatUserMapSchema, ChatUserMapSchema]):
    @classmethod
    def get_chat_user_map_by_chat_id(cls, chat_id: int, db: Session):
        try:
            query = sa.select(ChatUserMap).filter(ChatUserMap.chat_id == chat_id)
            result = jsonable_encoder(db.execute(query).mappings().all())
            return result

        except Exception as e:
            raise e


CRUDChatUserMap = ChatUserMapCrud(ChatUserMap)
