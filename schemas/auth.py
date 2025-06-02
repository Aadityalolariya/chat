from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LoginSchema(BaseModel):
    password: str
    phone_number: Optional[str] = None
    email: Optional[str] = None


class SignupSchema(BaseModel):
    password: str
    first_name: str
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    created_on: Optional[datetime] = datetime.utcnow()


class DecodedToken(BaseModel):
    user_id: int
    hashed_password: str


class ValidateToken(BaseModel):
    token: str
