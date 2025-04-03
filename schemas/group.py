import datetime

from pydantic import BaseModel
from typing import Optional


class GroupSchema(BaseModel):
    code: str
