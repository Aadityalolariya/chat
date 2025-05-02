from models.MessageSeenStatus import MessageSeenStatus
from schemas import MessageSeenStatusSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from typing import List


class MessageSeenStatusCrud(BaseCrud[MessageSeenStatus, MessageSeenStatusSchema, MessageSeenStatusSchema]):
    @classmethod
    def get_by_message_id(cls, db: Session, message_id: List[int] = None):
        try:
            query = sa.select(MessageSeenStatus.seen_status, MessageSeenStatus.id, MessageSeenStatus.message_id)
            if message_id:
                query = query.filter(MessageSeenStatus.message_id.in_(message_id))

            result = jsonable_encoder(db.execute(query).mappings().all())
            return result

        except Exception as e:
            raise e


CRUDMessageSeenStatus = MessageSeenStatusCrud(MessageSeenStatus)
