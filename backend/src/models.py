from sqlalchemy import Column, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    sign_in_count = Column(Integer, default=0)


class GlobalSignInCount(Base):
    __tablename__ = "global_sign_in_count"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)
