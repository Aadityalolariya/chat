from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from utils import decode_token, create_response
import service
from sqlalchemy.orm import Session
from fastapi import status
from schemas import CreateChatSchema
from db import get_db


chat_router = APIRouter(prefix='/chat', tags=['Chat APIs'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@chat_router.get('/fetch')
def get_all_chats():
    return {"result": "chats"}


@chat_router.post('/create_chat')
def api_create_chat(request: CreateChatSchema, db: Session = Depends(get_db), token: str = Security(oauth2_scheme)):
    try:
        result = service.create_new_chat(request=request, db=db, token=token)
        db.commit()
        return result
    except Exception as e:
        return create_response(result=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
