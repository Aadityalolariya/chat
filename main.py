from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
import uvicorn
from settings import WEB_PORT
from controller import chat_router, auth_router, message_router, user_router
from websocket import ConnectionManager
from sqlalchemy.orm import Session
from db import get_db
from service import user_disconnected_from_websocket, user_connected_to_websocket
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include all the required routes
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(message_router)
app.include_router(user_router)

# creating websocket manager object
manager = ConnectionManager()

# ping endpoint
@app.get('/ping')
def print_hi():
    return {"result": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id, db: Session = Depends(get_db)):
    await manager.connect(websocket, user_id=user_id)
    user_connected_to_websocket(user_id=user_id, db=db)
    print(f"connection request in ws for user {user_id}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"received data: {data}")

            # await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        print("client disconnected from ws")
        manager.disconnect(websocket, user_id)
        user_disconnected_from_websocket(user_id=user_id, db=db)
        # await manager.broadcast("A client disconnected")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=WEB_PORT, reload=True, use_colors=True)

