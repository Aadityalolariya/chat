from models.Chat import Chat
from models.User import User
from models.ChatUserMap import ChatUserMap
from schemas import ChatSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder


class ChatCrud(BaseCrud[Chat, ChatSchema, ChatSchema]):
    @classmethod
    def get_chats_for_user(cls, user_id: int, db: Session):
        try:
            query = (sa.select(Chat.id, Chat.chat_name, Chat.created_on, Chat.is_group_chat, Chat.admin_user_id,
                               ChatUserMap.id.label("chat_user_id"))
                     .join(ChatUserMap, ChatUserMap.chat_id == Chat.id)
                     .filter(ChatUserMap.user_id == user_id))

            result = jsonable_encoder(db.execute(query).mappings().all())

            chats = {}
            users = {}
            chat_user = {}
            for record in result:
                if record['id'] not in chats:
                    chats[record['id']] = {
                        "id": record['id'],
                        "chat_name": record['chat_name'],
                        "created_on": record['created_on'],
                        "is_group_chat": record['is_group_chat'],
                        "admin_user_id": record['admin_user_id']
                    }

            user_query = (sa.select(Chat.id, User.first_name, User.last_name, User.display_name, User.is_logged_in,
                                   User.currently_opened_chat_id, User.id.label("user_id"), User.phone_number,
                                   User.email)
                          .join(ChatUserMap, ChatUserMap.chat_id == Chat.id)
                          .join(User, User.id == ChatUserMap.user_id)
                          .filter(Chat.id.in_(list(chats.keys()))))

            user_result = jsonable_encoder(db.execute(user_query).mappings().all())

            for record in user_result:
                if record['user_id'] == user_id:
                    continue
                if record['user_id'] not in users:
                    users[record['user_id']] = {
                        "first_name": record['first_name'],
                        "last_name": record['last_name'],
                        "display_name": record['display_name'],
                        "is_logged_in": record['is_logged_in'],
                        "currently_opened_chat_id": record['currently_opened_chat_id'],
                        "id": record['user_id'],
                        "phone_number": record['phone_number'],
                        "email": record['email']
                    }
                if record['id'] not in chat_user:
                    chat_user[record['id']] = record['first_name'] + ' ' + record['last_name']
                else:
                    chat_user[record['id']] = chat_user[record['id']] + "," + record['first_name'] + ' ' + record[
                        'last_name']

            for chat_id, details in chats.items():
                if details['chat_name'] is None:
                    details['chat_name'] = chat_user[chat_id]

            result = {
                "chats": list(chats.values()),
                "users": list(users.values())
            }
            return result
        except Exception as e:
            print(e)
            raise e


CRUDChat = ChatCrud(Chat)
