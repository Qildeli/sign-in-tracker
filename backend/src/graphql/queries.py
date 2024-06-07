from typing import List

import strawberry
from sqlalchemy.orm import Session

from src.database import get_db
from src.graphql.types import UserType
from src.models import GlobalSignInCount, User


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[UserType]:
        db: Session = next(get_db())
        users = db.query(User).all()
        return [
            UserType(id=user.id, email=user.email, sign_in_count=user.sign_in_count)
            for user in users
        ]

    @strawberry.field
    def personal_sign_in_count(self, info) -> int:
        user_id = info.context["user_id"]
        db: Session = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        return user.sign_in_count if user else 0

    @strawberry.field
    def global_sign_in_count(self) -> int:
        db: Session = next(get_db())
        global_sign_in_count = db.query(GlobalSignInCount).first()
        return global_sign_in_count.count if global_sign_in_count else 0
