import jwt
import bcrypt
from datetime import datetime
from settings import SECRET_KEY  # Import your secret key
from fastapi.responses import JSONResponse
from fastapi import status
from typing import Dict, Union, List, Any
from sqlalchemy.orm import Session
from schemas import DecodedToken

ALGORITHM = "HS256"


# Function to hash passwords
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


# Function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# Function to generate token (with encrypted password)
def generate_token(user_id: int, password: str) -> str:
    hashed_password = hash_password(password)  # Hash the password
    payload = {
        "user_id": user_id,
        "hashed_password": hashed_password,
        "iat": datetime.utcnow()  # Issued at time (optional)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# Function to decode token and verify user credentials
def decode_token(token: str) -> DecodedToken:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        hashed_password = payload["hashed_password"]
        return DecodedToken(user_id=user_id, hashed_password=hashed_password)

    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.InvalidTokenError as e:
        raise e


def create_response(result: Any, status_code=status.HTTP_200_OK, is_error=False):
    if not is_error:
        response = JSONResponse(
            content={"status": "success", "result": result},
            status_code=status_code
        )
    else:
        response = JSONResponse(
            content={"status": "failure", "result": result},
            status_code=status_code
        )
    return response
