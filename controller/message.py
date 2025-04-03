from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from utils import decode_token, create_response
import service
from sqlalchemy.orm import Session
from fastapi import status
from schemas import CreateMessageSchema
from db import get_db


message_router = APIRouter(prefix='/message', tags=['Message APIs'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@message_router.post('/create_message/{chat_id}')
def api_create_message(chat_id: int, request: CreateMessageSchema, db: Session = Depends(get_db),
                       token: str = Security(oauth2_scheme)):
    try:
        result = service.create_new_message(request=request, db=db, token=token, chat_id=chat_id)
        db.commit()
        return result
    except Exception as e:
        return create_response(result=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, is_error=True)
