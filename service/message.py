from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDMessage
from models.User import User
from schemas import *
from fastapi import status
from dao import *
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
        chat_user_map_list = CRUDChatUserMap.get_chat_user_map_by_chat_id(db=db, chat_id=chat_id)
        seen_status_dict = {}
        for user_map in chat_user_map_list:
            if int(user_map['user_id']) != decoded_token.user_id:
                seen_status_dict[user_map['user_id']] = {

                }



    except Exception as e:
        raise e
