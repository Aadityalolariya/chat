import json

from fastapi import UploadFile
from fastapi.responses import FileResponse
from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDMessage, CRUDMessageSeenStatus, CRUDDocument, CRUDUnseenMessages
import os
from schemas import *
from fastapi import status
from dao import *
from utils import get_current_time
from constants import *
from uuid import uuid4
import shutil

# import sys
#
# sys.path.append(os.getcwd())

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_new_message(request: CreateMessageSchema, db: Session, token: str, chat_id: int, manager):
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
        message_request_obj = MessageSchema(chat_id=chat_id, content=request.content, sender_id=decoded_token.user_id,
                                    document_id=request.document_id, parent_message_id=request.parent_message_id,
                                    reference_message_id=request.reference_message_id)

        message_obj = CRUDMessage.create(obj_in=message_request_obj, db=db)

        # set seen status for receivers
        # fetch all the receivers
        chat_user_map_list = CRUDChatUserMap.get_chat_user_map_details_by_chat_id(db=db, chat_id=chat_id)
        seen_status_dict = {}
        current_time = get_current_time()
        unseen_message_list = []

        for user_map in chat_user_map_list:
            seen_status = MSG_PENDING_STATUS
            if user_map['is_logged_in'] is True:
                seen_status = MSG_SENT_STATUS
                if user_map['currently_opened_chat_id'] == chat_id:
                    seen_status = MSG_SEEN_STATUS

            if seen_status != MSG_SEEN_STATUS:
                unseen_obj = UnseenMessagesSchema(message_id=message_obj.id, chat_id=chat_id, user_id=user_map['user_id'])
                CRUDUnseenMessages.create(db=db, obj_in=unseen_obj)

            seen_status_dict[user_map['user_id']] = {
                "ts": current_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "status": seen_status
            }

        msg_seen_status_obj_in = MessageSeenStatusSchema(message_id=message_obj.id, seen_status=json.dumps(seen_status_dict))
        msg_seen_status_obj = CRUDMessageSeenStatus.create(db=db, obj_in=msg_seen_status_obj_in)

        resp = {
            "chat_id": chat_id,
            'message_id': message_obj.id,
            'message_ref_id': message_obj.reference_message_id,
            'parent_message_id': message_obj.parent_message_id,
            'document_id': message_obj.document_id,
            'content': message_obj.content,
            'sender_id': message_obj.sender_id,
            'created_on': message_obj.created_on.strftime('%Y-%m-%dT%H:%M:%S')
        }

        ws_data = {
            "topic": constants.TOPIC_MESSAGE_SENT,
            "data": resp
        }
        if chat_user_map_list:
            for record in chat_user_map_list:
                user = record['user_id']
                if user == decoded_token.user_id:
                    continue

                # send message through ws to active users in this chat
                if user in manager.active_connections:
                    await manager.send_personal_message(websocket=manager.active_connections[user],
                                                        message=json.dumps(ws_data))

        return create_response(result=resp)

    except Exception as e:
        raise e


def upload_file(file: UploadFile, db: Session, token: str):
    """
    store the file in server and add entry in document
    """
    try:
        filename = f"{uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        size_in_bytes = os.path.getsize(filepath)

        # entry in document table
        doc_obj_in = DocumentSchema(document_path=filepath, document_size=size_in_bytes)
        document_obj = CRUDDocument.create(db=db, obj_in=doc_obj_in)

        resp = {
            "document_id": document_obj.id,
            "document_size": document_obj.document_size
        }

        return create_response(result=resp)

    except Exception as e:
        raise e


def get_document(id: int, token: str, db: Session):
    try:
        doc_obj = CRUDDocument.get_by_id(db=db, id=id)

        filepath = os.path.join(os.getcwd(), doc_obj.document_path)

        if not os.path.isfile(filepath):
            return create_response(result={"error": "file doesn't exists"}, is_error=True)

        return FileResponse(filepath)
    except Exception as e:
        print(e)
        raise e


def fetch_message_service(request: FetchMessagesSchema, token: str, db: Session):
    try:
        decoded_token = decode_token(token=token)
        result = fetch_messages(db=db, chat_id=request.chat_id, offset=request.offset, limit=request.limit)
        return create_response(result=result)
    except Exception as e:
        return create_response(result=str(e), is_error=True)