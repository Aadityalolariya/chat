from pydantic import BaseModel
from typing import List, Optional, ByteString
from datetime import datetime


class DocumentSchema(BaseModel):
    document_path: str
    document_type_id: Optional[int] = None
    document_size: Optional[int] = None
