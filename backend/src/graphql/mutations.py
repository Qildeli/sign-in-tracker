import strawberry
from sqlalchemy.orm import Session

from src.auth import get_password_hash, verify_password
from src.database import get_db
from src.graphql.types import (
    LoginInput,
    LoginResponse,
    RegisterInput,
    RegisterResponse,
    UserType,
)
from src.JWT import create_access_token
from src.main import clients
from src.models import GlobalSignInCount, User


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, input: RegisterInput) -> RegisterResponse:
        db: Session = next(get_db())
        hashed_password = get_password_hash(input.password)
        new_user = User(email=input.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token = create_access_token(data={"sub": str(new_user.id)})
        user_type = UserType(
            id=new_user.id, email=new_user.email, sign_in_count=new_user.sign_in_count
        )
        return RegisterResponse(user=user_type, access_token=access_token)

    @strawberry.mutation
    async def login(self, input: LoginInput) -> LoginResponse:
        db: Session = next(get_db())
        user = db.query(User).filter(User.email == input.email).first()
        if not user or not verify_password(input.password, user.password):
            raise Exception("Invalid credentials")
        access_token = create_access_token(data={"sub": str(user.id)})
        user.sign_in_count += 1

        global_sign_in_count = db.query(GlobalSignInCount).first()
        global_sign_in_count.count += 1

        db.commit()

        if global_sign_in_count.count >= 5:
            # Notify all clients about the threshold
            message = "Global sign-in count has reached 5!"
            for client in clients:
                await client.send_text(message)

        user_type = UserType(
            id=user.id, email=user.email, sign_in_count=user.sign_in_count
        )
        return LoginResponse(user=user_type, access_token=access_token)
