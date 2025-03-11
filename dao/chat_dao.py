from models import *
from crud import CRUDChatUserMap
from sqlalchemy.orm import Session
from typing import List
import sqlalchemy as sa
from schemas import ChatUserMapSchema
from fastapi.encoders import jsonable_encoder


def get_dual_chats_for_given_ids(user_ids: List[int], db: Session) -> List[dict]:
    try:
        query = (
            sa.select(Chat.id, Chat.chat_name, Chat.is_group_chat)
            .join(ChatUserMap, ChatUserMap.chat_id == Chat.id)
            .filter(ChatUserMap.user_id.in_(user_ids))
        )
        result = jsonable_encoder(db.execute(query).mappings().all())
        return result
    except Exception as e:
        raise e


def map_user_with_chat(user_ids: List[int], chat_id: int, db: Session) -> List[ChatUserMap]:
    try:
        response = []
        for user_id in user_ids:
            obj_in = ChatUserMapSchema(user_id=user_id, chat_id=chat_id)
            result = CRUDChatUserMap.create(db=db, obj_in=obj_in)
            response.append(result)

        return response

    except Exception as e:
        raise e
