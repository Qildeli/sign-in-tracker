from fastapi import Request, WebSocket

from src.utils.auth import decode_token


def get_context(request: Request = None, websocket: WebSocket = None):
    """
    Extracts the authorization token from the headers of the request,
    decodes the token to retrieve the user_id and returns it in the context.
    """

    token = None
    if request:
        authorization: str = request.headers.get("Authorization")
        if authorization:
            token = authorization.split(" ")[1]
    elif websocket:
        authorization: str = websocket.headers.get("Authorization")
        if authorization:
            token = authorization.split(" ")[1]

    user_id = None
    if token:
        user_id = decode_token(token)

    return {"user_id": user_id}
