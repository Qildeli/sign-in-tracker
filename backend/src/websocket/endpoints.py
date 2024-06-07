import json

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.crud import get_user_by_id
from src.database import get_db
from src.models import GlobalSignInCount
from src.utils.auth import decode_token
from src.websocket.connection_manager import manager


async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    """Method to handle incoming WebSocket connections and messages"""

    await websocket.accept()
    user = None
    try:
        # Authenticate the user
        message = await websocket.receive_text()
        data = json.loads(message)
        if data.get("type") == "authenticate" and "token" in data:
            user_id = decode_token(data["token"])
            if not user_id:
                await websocket.close()
                return

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

            # Keep the connection open
            while True:
                await websocket.receive_text()

    except WebSocketDisconnect:
        if user:
            manager.disconnect(websocket, str(user.id))

    except Exception as e:
        print(f"Exception: {e}")
        if user:
            manager.disconnect(websocket, str(user.id))
        await websocket.close()
