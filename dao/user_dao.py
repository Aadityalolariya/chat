import json

from models import *
from crud import CRUDChatUserMap, CRUDMessageSeenStatus
from sqlalchemy.orm import Session, aliased
from typing import List, Dict, Optional
import sqlalchemy as sa
from schemas import ChatUserMapSchema
from fastapi.encoders import jsonable_encoder
from utils import get_current_time
from sqlalchemy import func


def get_user_contacts_by_id(user_id: int, db: Session) -> Optional[int]:
    try:
        ChatUserMapAlias1 = aliased(ChatUserMap)
        query = (
            sa.select(ChatUserMap.id, User.id.label('user_id'), User.first_name, User.last_name,
                      User.phone_number, User.email)
            .join(ChatUserMapAlias1, ChatUserMapAlias1.chat_id == ChatUserMap.chat_id)
            .join(User, User.id == ChatUserMapAlias1.user_id)
            .filter(ChatUserMap.user_id == user_id)
        )
        result = db.execute(query).all()
        user_detail = dict()
        for record in result:
            # we won't return the current user
            if record.user_id == user_id:
                continue
            if record.user_id not in user_detail:
                user_detail[record.user_id] = {
                    "id": record.user_id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "phone_number": record.phone_number,
                    "email": record.email
                }

        return list(user_detail.values())

    except Exception as e:
        raise e
