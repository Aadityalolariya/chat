from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDChat
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
    decoded_token = decode_token(token=token)

    if len(request.user_ids) == 2:
        response = handle_dual_chat_creation(request=request, db=db)
    else:
        response = handle_group_chat_creation(request=request, db=db, admin_user=decoded_token.user_id)

    return create_response(result=response, is_error=False)


def handle_dual_chat_creation(request: CreateChatSchema, db: Session):
    existing_chat = get_dual_chats_for_given_ids(user_ids=request.user_ids, db=db)
    if not existing_chat:
        obj_in = ChatSchema(is_group_chat=False)
        created_chat: Chat = CRUDChat.create(db=db, obj_in=obj_in)

        # mapping the users and created chat
        map_user_with_chat(user_ids=request.user_ids, db=db, chat_id=created_chat.id)

        return {
            "id": created_chat.id,
            "chat_name": created_chat.chat_name,
            "is_group_chat": created_chat.is_group_chat
        }
    return {
        "id": existing_chat[0]['id'],
        "chat_name": existing_chat[0]['chat_name'],
        "is_group_chat": existing_chat[0]['is_group_chat']
    }


def handle_group_chat_creation(request: CreateChatSchema, db: Session, admin_user: int):
    try:
        # create chat
        obj_in = ChatSchema(is_group_chat=True, chat_name=request.chat_name, admin_user_id=admin_user)
        created_chat: Chat = CRUDChat.create(db=db, obj_in=obj_in)

        # mapping the users and created chat
        map_user_with_chat(user_ids=request.user_ids, db=db, chat_id=created_chat.id)

        return {
            "id": created_chat.id,
            "admin_user_id": created_chat.admin_user_id,
            "chat_name": created_chat.chat_name,
            "is_group_chat": created_chat.is_group_chat
        }

    except Exception as e:
        raise e
