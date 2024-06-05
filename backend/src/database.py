from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.models import GlobalSignInCount
from src.settings import SQLALCHEMY_DATABASE_URL

load_dotenv()


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db: Session = SessionLocal()
    if not db.query(GlobalSignInCount).first():
        global_count = GlobalSignInCount(count=0)
        db.add(global_count)
        db.commit()


init_db()
