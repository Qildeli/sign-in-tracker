import os

from fastapi.middleware.cors import CORSMiddleware

CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_SETTINGS["allow_origins"],
        allow_credentials=CORS_SETTINGS["allow_credentials"],
        allow_methods=CORS_SETTINGS["allow_methods"],
        allow_headers=CORS_SETTINGS["allow_headers"],
    )


# database config
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# security config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
