from pydantic import BaseModel


class UnseenMessagesSchema(BaseModel):
    message_id: int
    chat_id: int
    user_id: int
