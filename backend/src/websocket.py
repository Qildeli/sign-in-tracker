import json
from typing import Dict, List

from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from src.database import get_db
from src.utils.auth import decode_token
from src.models import GlobalSignInCount


class ConnectionManager:
    """Websocket connection manager"""

    def __init__(self):
        """Keys are user IDs, values are lists of WebSocket connections"""

        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Adds a WebSocket connection to the list of active connections for a user"""

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Removes a WebSocket connection for a user"""

        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def broadcast(self, message: str):
        """Sends a message to all active connections"""

        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_text(message)

    async def send_personal_update(self, user_id: str, message: str):
        """Sends a message to all connections of a specific user"""

        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    """Method to handle incoming WebSocket connections and messages"""

    await websocket.accept()
    try:
        message = await websocket.receive_text()
        data = json.loads(message)
        if data["type"] == "authenticate" and "token" in data:
            user_id = decode_token(data["token"])
            if not user_id:
                await websocket.close()
                return

            from src.crud import get_user_by_id

            user = get_user_by_id(db, user_id)
            if not user:
                await websocket.close()
                return

            await manager.connect(websocket, str(user.id))
            global_sign_in_count = db.query(GlobalSignInCount).first()
            await websocket.send_text(
                json.dumps(
                    {
                        "type": "initial",
                        "globalSignInCount": global_sign_in_count.count,
                        "personalSignInCount": user.sign_in_count,
                    }
                )
            )

            while True:
                await websocket.receive_text()  # Keep the connection open

    except WebSocketDisconnect:
        manager.disconnect(websocket, str(user.id))
