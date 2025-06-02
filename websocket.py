from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[int(user_id)] = websocket
        print(f"connection request accepted for user: {user_id}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections.pop(int(user_id))
        print(f"user: {user_id} disconnected")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for user, connection in self.active_connections.items():
            await connection.send_text(message)
