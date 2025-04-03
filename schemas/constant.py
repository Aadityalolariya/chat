import datetime

from pydantic import BaseModel
from typing import Optional


class ConstantSchema(BaseModel):
    group_id: int
    code: str
