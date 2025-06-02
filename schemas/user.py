from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserSchema(BaseModel):
    password: str
    first_name: str
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    created_on: Optional[datetime] = datetime.utcnow()
    profile_picture: Optional[str] = None
    description: Optional[str] = None
    is_logged_in: Optional[bool] = True
    currently_opened_chat_id: Optional[int] = None


class SearchUserSchema(BaseModel):
    search: Optional[str] = None


