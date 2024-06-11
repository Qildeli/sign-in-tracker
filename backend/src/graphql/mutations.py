import strawberry
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.crud import create_user, get_user_by_email, get_user_by_id
from src.database import get_db
from src.graphql.types import (
    LoginInput,
    LoginResponse,
    RefreshTokenRequest,
    RegisterInput,
    RegisterResponse,
    UserInput,
    UserType,
)
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from src.utils.helpers import increment_counts_and_broadcast


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, input: RegisterInput) -> RegisterResponse:
        # Validate input
        UserInput(email=input.email, password=input.password)

        db: Session = next(get_db())
        user = create_user(db, input)

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # Increment counts and broadcast updates
        user, global_count = await increment_counts_and_broadcast(db, user)

        user_type = UserType(
            id=user.id, email=user.email, sign_in_count=user.sign_in_count
        )
        return RegisterResponse(
            user=user_type, access_token=access_token, refresh_token=refresh_token
        )

    @strawberry.mutation
    async def login(self, input: LoginInput) -> LoginResponse:
        # Validate input
        UserInput(email=input.email, password=input.password)

        db: Session = next(get_db())
        user = get_user_by_email(db, input.email)
        if not user or not verify_password(input.password, user.password):
            raise Exception("Invalid credentials")

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # Increment counts and broadcast updates
        user, global_count = await increment_counts_and_broadcast(db, user)

        user_type = UserType(
            id=user.id, email=user.email, sign_in_count=user.sign_in_count
        )
        return LoginResponse(
            user=user_type, access_token=access_token, refresh_token=refresh_token
        )

    @strawberry.mutation
    def refresh_token(self, input: RefreshTokenRequest) -> LoginResponse:
        user_id = decode_token(input.refresh_token)

        db: Session = next(get_db())
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        new_access_token = create_access_token(data={"sub": user_id})
        new_refresh_token = create_refresh_token(data={"sub": user_id})

        return LoginResponse(
            user=UserType(id=user.id, email=user.email, sign_in_count=user.sign_in_count),
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
