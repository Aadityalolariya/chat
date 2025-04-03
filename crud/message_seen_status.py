from models.MessageSeenStatus import MessageSeenStatus
from schemas import MessageSeenStatusSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa


class MessageSeenStatusCrud(BaseCrud[MessageSeenStatus, MessageSeenStatusSchema, MessageSeenStatusSchema]):
    pass


CRUDMessageSeenStatus = MessageSeenStatusCrud(MessageSeenStatus)
