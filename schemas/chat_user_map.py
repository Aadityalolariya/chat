import datetime

from pydantic import BaseModel
from typing import Optional


class ChatUserMapSchema(BaseModel):
    user_id: Optional[int]
    chat_id: Optional[int]
    last_seen_timestamp: Optional[datetime.datetime] = None
