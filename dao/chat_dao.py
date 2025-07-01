import json

from models import *
from crud import CRUDChatUserMap, CRUDMessageSeenStatus
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import sqlalchemy as sa
from schemas import ChatUserMapSchema
from fastapi.encoders import jsonable_encoder
from utils import get_current_time
from sqlalchemy import func


def get_dual_chats_for_given_ids(user_ids: List[int], db: Session) -> Optional[int]:
    try:
        query = (
            sa.select(ChatUserMap.chat_id, ChatUserMap.user_id)
            .filter(ChatUserMap.user_id.in_(user_ids))
        )
        result = db.execute(query).all()
        user_chat_sets = {}
        for record in result:
            if record.user_id not in user_chat_sets:
                user_chat_sets[record.user_id] = set()
            user_chat_sets[record.user_id].add(record.chat_id)

        if len(list(user_chat_sets.keys())) < 2:
            return None

        common_chats = user_chat_sets[user_ids[0]]
        for user, chats in user_chat_sets.items():
            common_chats = common_chats.intersection(chats)
        if len(common_chats) > 1:
            return list(common_chats)[0]
        else:
            return None

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


def update_message_seen_status(db: Session, user_id: int, status: int, message_seen_status_list: List[dict]):
    try:
        current_time = get_current_time()
        for record in message_seen_status_list:
            seen_status = json.loads(record['seen_status'])
            if str(user_id) in seen_status:
                seen_status[str(user_id)] = {
                    "ts": current_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    "status": status
                }
            seen_status_dict = json.dumps(seen_status)
            CRUDMessageSeenStatus.update(db=db, obj_id=record['id'], obj_in={"seen_status": seen_status_dict})
    except Exception as e:
        print(e)
        raise e
