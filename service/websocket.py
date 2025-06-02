import json

import constants
from crud import CRUDUser, CRUDMessage
from models import User
from sqlalchemy.orm import Session
from schemas import WebsocketDataSchema
from websocket import ConnectionManager
import dao

def user_connected_to_websocket(user_id: int, db: Session):
    try:
        CRUDUser.update(db=db, obj_id=int(user_id), obj_in={"is_logged_in": True})
        db.commit()
        print("user logged in")

    except Exception as e:
        print(e)
        raise e


def user_disconnected_from_websocket(user_id: int, db: Session):
    try:
        CRUDUser.update(db=db, obj_id=user_id, obj_in={"is_logged_in": False, "currently_opened_chat_id": None})
        db.commit()
        print("user logged in")

    except Exception as e:
        print(e)
        raise e


async def send_data_through_ws(user_id: int, data: str, db: Session, manager: ConnectionManager):
    try:
        ws_msg = json.loads(data)
        ws_data = WebsocketDataSchema(**ws_msg)

        if ws_data.topic == constants.TOPIC_MESSAGE_SENT:
            pass
            # # send message data to the users of the chat
            # message_id = ws_data.data['message_id']
            # timestamp = ws_data.data['timestamp']
            #
            # # get message data by id
            # msg_user_data = dao.get_message_and_user_data(message_id=message_id, db=db)
            #
            # if msg_user_data:
            #     message_data = {
            #         "id": msg_user_data[0]['id'],
            #         "chat_id": msg_user_data[0]['chat_id'],
            #         "thread_id": msg_user_data[0]['thread_id'],
            #         "reference_message_id": msg_user_data[0]['reference_message_id'],
            #         "sender_id": msg_user_data[0]['sender_id'],
            #         "created_on": msg_user_data[0]['created_on'].strftime('%Y-%m-%d %H:%M:%S')
            #     }
            #
            #     for record in msg_user_data:
            #         user = record['user_id']
            #         if user in manager.active_connections:
            #             await manager.send_personal_message(websocket=manager.active_connections[user],
            #                                                 message=json.dumps(message_data))

        elif ws_data.topic == constants.TOPIC_CHAT_SEEN:
            pass
        else:
            print("Invalid topic!!!")
    except Exception as e:
        print(e)
        raise e
