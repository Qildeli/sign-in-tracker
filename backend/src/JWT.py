from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt

from src.settings import ACCESS_TOKEN_EXPIRATION, ALGORITHM, SECRET_KEY

load_dotenv()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise Exception("Invalid token")
