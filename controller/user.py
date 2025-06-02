from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from utils import decode_token, create_response
from crud.chat import CRUDChat
import service
from sqlalchemy.orm import Session
from fastapi import status
from schemas import SearchUserSchema
from db import get_db


user_router = APIRouter(prefix='/user', tags=['User APIs'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.post('/search_user')
def api_get_user(request: SearchUserSchema, db: Session = Depends(get_db), token: str = Security(oauth2_scheme)):
    try:
        result = service.search_user(request=request, db=db, token=token)
        return result
    except Exception as e:
        return create_response(result=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, is_error=True)
