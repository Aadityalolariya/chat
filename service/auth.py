from utils import decode_token, hash_password, verify_password, create_response, generate_token
from sqlalchemy.orm import Session
from crud import CRUDUser
from models.User import User
from schemas import *
from fastapi import status


def login_user(request: LoginSchema, db: Session) -> bool:
    try:
        if request.email is None and request.phone_number is None:
            return create_response(result="Provider at least one of the following fields: phone, email",
                                   status_code=status.HTTP_400_BAD_REQUEST, is_error=True)

        # get the user with given phone/email
        user_obj = CRUDUser.get_by_email_phone(db=db, phone=request.phone_number, email=request.email)

        if user_obj is None:
            return create_response(result="User not found", status_code=status.HTTP_400_BAD_REQUEST, is_error=True)

        is_password_matching = verify_password(plain_password=request.password, hashed_password=user_obj.password)

        if not is_password_matching:
            return create_response(result="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED, is_error=True)

        # update the user last opened date
        CRUDUser.update(db=db, obj_id=user_obj.id, obj_in={"is_logged_in": True})

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
            "theme_id": user_obj.theme_id,
            "last_opened_date": str(user_obj.last_opened_date),
            "created_on": str(user_obj.created_on),
            "token": generate_token(user_id=user_obj.id, password=request.password)
        }
        return create_response(result=response)

    except Exception as e:
        return create_response(result="Error occurred", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, is_error=True)


def signup_user(user_details: SignupSchema, db: Session):
    try:
        # user should provide at least one among phone and email
        if user_details.email is None and user_details.phone_number is None:
            return create_response(result="Missing arguments", is_error=True)

        # get the user with given user id
        user_obj = CRUDUser.get_by_email_phone(db=db, phone=user_details.phone_number, email=user_details.email)

        if user_obj is not None:
            return create_response(result="Duplicate user found", is_error=True)

        user_obj = UserSchema(
            first_name=user_details.first_name,
            last_name=user_details.last_name,
            password=hash_password(password=user_details.password),
            phone_number=user_details.phone_number,
            email=user_details.email
        )

        created_user: User = CRUDUser.create(db=db, obj_in=user_obj)

        response = {
            "id": created_user.id,
            "first_name": created_user.first_name,
            "last_name": created_user.last_name,
            "email": created_user.email,
            "phone_number": created_user.phone_number,
            "token": generate_token(user_id=created_user.id, password=user_details.password)
        }

        return create_response(result=response, is_error=False)
    except Exception as e:
        raise e
