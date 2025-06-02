from models.User import User
from schemas import UserSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa


class UserCrud(BaseCrud[User, UserSchema, UserSchema]):

    @classmethod
    def get_by_email_phone(cls, db: Session, email: str, phone: str) -> User | None:
        return (db.query(User.first_name, User.id, User.phone_number, User.last_name, User.display_name, User.created_on,
                         User.email, User.is_logged_in, User.password, User.currently_opened_chat_id, User.description,
                         User.profile_picture)
                .filter(sa.or_(User.email == email, User.phone_number == phone))
                .first())


CRUDUser = UserCrud(User)
