from fastapi import APIRouter


chat_router = APIRouter(prefix='/chat', tags=['Chat APIs'])


@chat_router.get('/')
def get_all_chats():
    return {"result": "chats"}
