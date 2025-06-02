import constants
from models import *
from crud import CRUDChatUserMap
from sqlalchemy.orm import Session
from typing import List
import sqlalchemy as sa
from schemas import ChatUserMapSchema
from fastapi.encoders import jsonable_encoder


def get_receiver_data_for_seen_status(user_id: int, chat_id: int, db: Session) -> List[dict]:
    try:
        query = (
            sa.select(User.is_logged_in, User.id, User.currently_opened_chat_id)
            .join(ChatUserMap, ChatUserMap.chat_id == Chat.id)
            .filter(ChatUserMap.user_id == user_id)
        )
        result = jsonable_encoder(db.execute(query).mappings().all())
        return result
    except Exception as e:
        raise e


def fetch_messages(db: Session, chat_id: int, offset: int = constants.MESSAGE_OFFSET,
                   limit: int = constants.MESSAGE_LIMIT):
    try:
        query = (sa.select(Message.id, Message.sender_id, Message.document_id, Message.content, Message.reference_message_id,
                           Message.chat_id, Message.thread_id, Message.created_on).filter(Message.chat_id == chat_id).order_by(Message.id).limit(limit)
                 .offset(offset))
        result = jsonable_encoder(db.execute(query).mappings().all())
        return result

    except Exception as e:
        raise e


def get_message_and_user_data(message_id, db: Session):
    try:
        query = (sa.select(Message.id, Message.thread_id, Message.chat_id, Message.reference_message_id,
                           Message.sender_id, Message.created_on, ChatUserMap.user_id)
                 .join(ChatUserMap, ChatUserMap.chat_id == Message.chat_id)
                 .filter(Message.id == message_id))
        result = jsonable_encoder(db.execute(query).mappings().all())
        return result
    except Exception as e:
        print(e)
        raise e