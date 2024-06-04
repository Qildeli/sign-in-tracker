from typing import List

import strawberry

from src.database import get_db
from src.graphql.types import UserType
from src.models import User


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[UserType]:
        db = next(get_db())
        users = db.query(User).all()
        return users
