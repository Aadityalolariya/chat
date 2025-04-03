import datetime

from pydantic import BaseModel
from typing import Optional


class MessageSeenStatusSchema(BaseModel):
    message_id: int
    seen_status: str
