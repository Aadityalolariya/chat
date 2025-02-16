from pydantic import BaseModel
from typing import List


class LoginSchema(BaseModel):
    password: str


class SignupSchema(BaseModel):
    password: str
    firstname: str
    lastname: str

