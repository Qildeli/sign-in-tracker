from typing import Dict, List

from fastapi import WebSocket


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
