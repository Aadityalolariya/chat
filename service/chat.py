import constants
from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDChat, CRUDUnseenMessages, CRUDMessageSeenStatus, CRUDUser
from models.User import User
from schemas import *
from fastapi import status
from dao import *


def create_new_chat(request: CreateChatSchema, db: Session, token: str):
    """
    1. if it is dual chat, check if the chat already exists. if yes, don't allow to create chat and throw error
    2. create a chat and map the given users in it
    :param request:
    :param db:
    :return:
    """
    try:

        decoded_token = decode_token(token=token)

        if not request.is_group_chat:
            response = handle_dual_chat_creation(request=request, db=db)
        else:
            response = handle_group_chat_creation(request=request, db=db, admin_user=decoded_token.user_id)

        return response

    except Exception as e:
        raise e


def handle_dual_chat_creation(request: CreateChatSchema, db: Session):
    if len(request.user_ids) > 2:
        return create_response(result="More than two users not allowed in dual chat", status_code=status.HTTP_400_BAD_REQUEST, is_error=True)
    existing_chat = get_dual_chats_for_given_ids(user_ids=request.user_ids, db=db)
    if not existing_chat:
        obj_in = ChatSchema(is_group_chat=False)
        created_chat: Chat = CRUDChat.create(db=db, obj_in=obj_in)

        # mapping the users and created chat
        map_user_with_chat(user_ids=request.user_ids, db=db, chat_id=created_chat.id)

        response = {
            "id": created_chat.id,
            "chat_name": created_chat.chat_name,
            "is_group_chat": created_chat.is_group_chat,
            "created_on": created_chat.created_on.strftime('%Y-%m-%dT%H:%M:%S')
        }
    else:
        chatObj = CRUDChat.get_by_id(db=db, id=existing_chat)
        response = {
            "id": chatObj.id,
            "chat_name": chatObj.chat_name,
            "is_group_chat": chatObj.is_group_chat,
            "created_on": chatObj.created_on.strftime('%Y-%m-%dT%H:%M:%S')
        }

    return create_response(result=response, is_error=False)


def handle_group_chat_creation(request: CreateChatSchema, db: Session, admin_user: int):
    try:
        # create chat
        obj_in = ChatSchema(is_group_chat=True, chat_name=request.chat_name, admin_user_id=admin_user)
        created_chat: Chat = CRUDChat.create(db=db, obj_in=obj_in)

        # mapping the users and created chat
        map_user_with_chat(user_ids=request.user_ids, db=db, chat_id=created_chat.id)

        response = {
            "id": created_chat.id,
            "admin_user_id": created_chat.admin_user_id,
            "chat_name": created_chat.chat_name,
            "is_group_chat": created_chat.is_group_chat,
            "created_on": created_chat.created_on.strftime('%Y-%m-%dT%H:%M:%S')
        }
        return create_response(result=response, is_error=False)

    except Exception as e:
        raise e


def open_chat(chat_id: int, db: Session, token: str):
    """
    1) mark the unseen messages for the given chat for the current user as seen
    2) update the current open chat of the current user
    3) fetch latest n messages for the chat
    """
    try:
        decoded_token = decode_token(token=token)
        user_id = decoded_token.user_id

        # deleting the records from unseen messages and updating status in message seen status
        unseen_messages = CRUDUnseenMessages.get_unseen_message_for_user(db=db, user_id=[user_id], chat_id=[chat_id])
        if unseen_messages:
            for unseen_msg in unseen_messages:
                CRUDUnseenMessages.delete(db=db, id=unseen_msg['id'])
                message_seen_status_list = CRUDMessageSeenStatus.get_by_message_id(db=db, message_id=[unseen_msg['message_id']])
                update_message_seen_status(db=db, user_id=user_id, status=constants.MSG_SEEN_STATUS,
                                           message_seen_status_list=message_seen_status_list)

        # update the user current open chat
        CRUDUser.update(db=db, obj_id=user_id, obj_in={"currently_opened_chat_id": chat_id})

        # fetch latest messages
        messages = fetch_messages(db=db, chat_id=chat_id, offset=0)

        resp = {
            "messages": messages,
            "chat_id": chat_id
        }
        return create_response(result=resp)

    except Exception as e:
        print(e)
        raise e


def fetch_chat(token: str, db: Session):
    try:
        decoded_token = decode_token(token=token)
        user_id = decoded_token.user_id
        result = CRUDChat.get_chats_for_user(user_id=user_id, db=db)
        return create_response(result=result)
    except Exception as e:
        raise e


def delete_chat(chat_id: int, db: Session, token: str):
    """
    - for group chat
        - TODO: handle this case
    - for dual chat
        - if both user delets the chat
            - delete chat user mapping
            - delete entries from unseen messages
            - delete records from message seen status
            - delete the messages of the chat
            - delete the associated documents
            - TODO: delete reactions and threads
        - if only one user deletes the chat:
            - delete chat user mapping
    :param chat_id:
    :param db:
    :param token:
    :return:
    """
    try:
        decoded_token = decode_token(token=token)
        user_id = decoded_token.user_id
        return create_response(result=result)
    except Exception as e:
        raise e
