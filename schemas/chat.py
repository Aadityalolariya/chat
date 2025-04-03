from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatSchema(BaseModel):
    chat_name: Optional[str] = None
    admin_user_id: Optional[int] = None
    is_group_chat: Optional[bool]
    created_on: Optional[datetime] = datetime.utcnow()


class CreateChatSchema(BaseModel):
    user_ids: List[int]                 # for group chat, its length will be greater than 1
    chat_name: Optional[str] = None     # in case of single chat, it will be empty
    is_group_chat: bool = False
