from models.UnseenMessages import UnseenMessages
from schemas import UnseenMessagesSchema
from crud import BaseCrud
from typing import List
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder


class UnseenMessagesCrud(BaseCrud[UnseenMessages, UnseenMessagesSchema, UnseenMessagesSchema]):
    @classmethod
    def get_unseen_message_for_user(cls,  db: Session, user_id: List[int] = None, chat_id: List[int] = None,
                                    message_id: List[int] = None):
        try:
            query = sa.select(UnseenMessages.chat_id, UnseenMessages.message_id, UnseenMessages.id,
                              UnseenMessages.user_id)
            if user_id:
                query = query.filter(UnseenMessages.user_id.in_(user_id))
            if chat_id:
                query = query.filter(UnseenMessages.chat_id.in_(chat_id))
            if message_id:
                query = query.filter(UnseenMessages.message_id.in_(message_id))

            result = jsonable_encoder(db.execute(query).mappings().all())
            return result

        except Exception as e:
            raise e


CRUDUnseenMessages = UnseenMessagesCrud(UnseenMessages)
