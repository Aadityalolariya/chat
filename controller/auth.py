from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from utils import decode_token, create_response
from fastapi import HTTPException
from fastapi import status
from schemas import LoginSchema

auth_router = APIRouter(prefix='/auth', tags=['Chat APIs'])

# OAuth2 scheme for extracting Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post('/login')
def api_login(request: LoginSchema, token: str = Depends(oauth2_scheme)):
    is_valid = decode_token(token=token, entered_password=request.password)
    if is_valid:
        return create_response(result="Logged in")
    else:
        return create_response(result="Invalid Token", status_code=status.HTTP_401_UNAUTHORIZED)


@auth_router.post('/signup')
def api_login(request: LoginSchema, token: str = Depends(oauth2_scheme)):
    is_valid = decode_token(token=token, entered_password=request.password)
    if is_valid:
        return create_response(result="Logged in")
    else:
        return create_response(result="Invalid Token", status_code=status.HTTP_401_UNAUTHORIZED)
