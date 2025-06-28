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
        group_key_expr = sa.func.coalesce(
            Message.parent_message_id, Message.id
        ).label('group_key')

        message_id_query = (sa.select(sa.func.group_concat(Message.id).label("message_id"), group_key_expr)
                            .filter(Message.chat_id == chat_id)
                            .group_by(group_key_expr)
                            .order_by(group_key_expr.desc())
                            # .limit(limit).offset(offset)
                            )
        print(f"message_id_query: {message_id_query}")

        message_ids = []
        non_paginated_msg = db.execute(message_id_query).all()

        non_paginated_msg = non_paginated_msg[offset:limit]

        for record in non_paginated_msg:
            msg_str: list = record.message_id.split(',')
            message_ids.extend(msg_str)
        print(f"message ids: {message_ids}")

        query = (sa.select(Message.id, Message.sender_id, Message.document_id, Message.content, Message.reference_message_id,
                           Message.chat_id, Message.parent_message_id, Message.created_on, Document.document_path,
                           Document.document_size)
                 .outerjoin(Document, Document.id == Message.document_id)
                 .filter(Message.id.in_(message_ids))
                 .order_by(Message.id))
        messages = jsonable_encoder(db.execute(query).mappings().all())
        result = {}

        for message in messages:
            message_id = message['parent_message_id']
            if message_id is None:
                message_id = message['id']
            if message['document_path']:
                message['document_name'] = message.pop('document_path')[constants.PREFIX_LENGTH_OF_DOCUMENT:]

            if message_id in result:
                result[message_id]['child_messages'].append(message)
            else:
                result[message_id] = message
                result[message_id]['child_messages'] = list()

        return list(result.values())

    except Exception as e:
        raise e


def get_message_and_user_data(message_id, db: Session):
    try:
        query = (sa.select(Message.id, Message.parent_message_id, Message.chat_id, Message.reference_message_id,
                           Message.sender_id, Message.created_on, ChatUserMap.user_id)
                 .join(ChatUserMap, ChatUserMap.chat_id == Message.chat_id)
                 .filter(Message.id == message_id))
        result = jsonable_encoder(db.execute(query).mappings().all())
        return result
    except Exception as e:
        print(e)
        raise e