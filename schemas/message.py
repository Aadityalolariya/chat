from pydantic import BaseModel
from typing import List, Optional, ByteString
from datetime import datetime


class MessageSchema(BaseModel):
    chat_id: int
    content: str
    sender_id: int
    document_id: Optional[int] = None
    parent_message_id: Optional[int] = None
    reference_message_id: Optional[int] = None
    created_on: Optional[datetime] = datetime.utcnow()


class CreateMessageSchema(BaseModel):
    content: str
    document_id: Optional[int] = None
    parent_message_id: Optional[int] = None
    reference_message_id: Optional[int] = None


class FetchMessagesSchema(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = 0
    chat_id: int
