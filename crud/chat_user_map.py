from models.ChatUserMap import ChatUserMap
from schemas import ChatUserMapSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from models import User

class ChatUserMapCrud(BaseCrud[ChatUserMap, ChatUserMapSchema, ChatUserMapSchema]):
    @classmethod
    def get_chat_user_map_details_by_chat_id(cls, chat_id: int, db: Session):
        try:
            query = (sa.select(ChatUserMap.chat_id, User.first_name, User.last_name, User.display_name,
                               User.is_logged_in, User.currently_opened_chat_id, User.id.label('user_id'))
                     .join(User, User.id == ChatUserMap.user_id)
                     .filter(ChatUserMap.chat_id == chat_id))
            result = jsonable_encoder(db.execute(query).mappings().all())
            return result

        except Exception as e:
            raise e


CRUDChatUserMap = ChatUserMapCrud(ChatUserMap)
