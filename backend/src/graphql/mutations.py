import strawberry
from sqlalchemy.orm import Session

from src.crud import create_user, get_user_by_email
from src.database import get_db
from src.graphql.types import (
    LoginInput,
    LoginResponse,
    RegisterInput,
    RegisterResponse,
    UserType,
)
from src.utils.auth import create_access_token, verify_password
from src.utils.helpers import increment_counts_and_broadcast


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, input: RegisterInput) -> RegisterResponse:
        db: Session = next(get_db())
        user = create_user(db, input)

        # Increment counts and broadcast updates
        user, global_count = await increment_counts_and_broadcast(db, user)

        access_token = create_access_token(data={"sub": str(user.id)})
        user_type = UserType(
            id=user.id, email=user.email, sign_in_count=user.sign_in_count
        )
        return RegisterResponse(user=user_type, access_token=access_token)

    @strawberry.mutation
    async def login(self, input: LoginInput) -> LoginResponse:
        db: Session = next(get_db())
        user = get_user_by_email(db, input.email)
        if not user or not verify_password(input.password, user.password):
            raise Exception("Invalid credentials")
        access_token = create_access_token(data={"sub": str(user.id)})

        # Increment counts and broadcast updates
        user, global_count = await increment_counts_and_broadcast(db, user)

        user_type = UserType(
            id=user.id, email=user.email, sign_in_count=user.sign_in_count
        )
        return LoginResponse(user=user_type, access_token=access_token)
