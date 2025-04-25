import json

from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDMessage, CRUDMessageSeenStatus
from models.User import User
from schemas import *
from fastapi import status
from dao import *
from utils import get_current_time
from constants import *


def create_new_message(request: CreateMessageSchema, db: Session, token: str, chat_id: int):
    """
    1. make entry in message table
    2. for all the receivers, create record in messageseenstatus table and set status as per the active status of the users
    :param request:
    :param token:
    :param db:
    :return:
    """
    try:
        # chat_id: int
        # content: str
        # sender_id: int
        # document_id: Optional[int] = None
        # thread_id: Optional[int] = None
        # reference_message_id: Optional[int] = None
        # created_on: Optional[datetime] = datetime.utcnow()

        decoded_token = decode_token(token=token)
        message_request_obj = MessageSchema(chat_id=request.chat_id, content=request.content, sender_id=decoded_token.user_id,
                                    document_id=request.document_id, thread_id=request.thread_id,
                                    reference_message_id=request.reference_message_id)

        message_obj = CRUDMessage.create(obj_in=message_request_obj, db=db)

        # set seen status for receivers
        # fetch all the receivers
        chat_user_map_list = CRUDChatUserMap.get_chat_user_map_details_by_chat_id(db=db, chat_id=chat_id)
        seen_status_dict = {}
        current_time = get_current_time()
        for user_map in chat_user_map_list:
            seen_status = MSG_PENDING_STATUS
            if user_map['is_logged_in'] is True:
                seen_status = MSG_SENT_STATUS
                if user_map['currently_opened_chat_id'] == chat_id:
                    seen_status = MSG_SEEN_STATUS

            seen_status_dict[user_map['user_id']] = {
                "ts": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": seen_status
            }

        msg_seen_status_obj_in = MessageSeenStatusSchema(message_id=message_obj.id, seen_status=json.dumps(seen_status_dict))
        msg_seen_status_obj = CRUDMessageSeenStatus.create(db=db, obj_in=msg_seen_status_obj_in)

        resp = {
            "chat_id": chat_id,
            'message_id': message_obj.id,
            'message_ref_id': message_obj.reference_message_id,
            'thread_id': message_obj.thread_id,
            'document_id': message_obj.document_id,
            'content': message_obj.content,
            'sender_id': message_obj.sender_id,
            'created_on': message_obj.created_on.strftime('%Y-%m-%d %H:%M:%S')
        }
        return create_response(result=resp)

    except Exception as e:
        raise e
