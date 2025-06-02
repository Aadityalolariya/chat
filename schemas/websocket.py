from pydantic import BaseModel


class WebsocketDataSchema(BaseModel):
    topic: str
    data: dict
