from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from utils import decode_token, create_response
import service
from sqlalchemy.orm import Session
from fastapi import status
from schemas import LoginSchema, SignupSchema
from db import get_db

auth_router = APIRouter(prefix='/auth', tags=['Chat APIs'])

# OAuth2 scheme for extracting Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post('/login')
def api_login(request: LoginSchema, db: Session = Depends(get_db)):
    try:
        result = service.login_user(request=request, db=db)
        db.commit()
        return result
    except Exception as e:
        return create_response(result=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@auth_router.post('/signup')
def api_signup(request: SignupSchema, db: Session = Depends(get_db)):
    try:
        result = service.signup_user(user_details=request, db=db)
        db.commit()
        return result
    except Exception as e:
        return create_response(result=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

