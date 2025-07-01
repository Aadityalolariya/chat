from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDUser
from schemas import *
from fastapi import status
import dao


def search_user(request: SearchUserSchema, db: Session, token: str) -> bool:
    try:
        decoded_token = decode_token(token=token)

        if request.search is None:
            return create_response(result="Provider valid search string",
                                   status_code=status.HTTP_400_BAD_REQUEST, is_error=True)

        # get the user with given phone/email
        user_obj = CRUDUser.get_by_email_phone(db=db, phone=request.search, email=request.search)

        if user_obj is None:
            return create_response(result="User not found", status_code=status.HTTP_400_BAD_REQUEST, is_error=True)

        response = {
            "id": user_obj.id,
            "phone_number": user_obj.phone_number,
            "email": user_obj.email,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "display_name": user_obj.display_name,
            "profile_picture": user_obj.profile_picture,
            "description": user_obj.description,
            "login_status_id": user_obj.is_logged_in,
            "created_on": str(user_obj.created_on),
        }
        return create_response(result=response)
    except Exception as e:
        return create_response(result="Error occurred", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, is_error=True)


def get_contact(token: str, db: Session):
    try:
        decoded_token = decode_token(token=token)
        result = dao.get_user_contacts_by_id(user_id=decoded_token.user_id, db=db)
        return create_response(result=result)

    except Exception as e:
        return create_response(result="Error occurred", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, is_error=True)