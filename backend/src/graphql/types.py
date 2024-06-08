import strawberry
from pydantic import BaseModel, EmailStr, Field, field_validator


# Pydantic model for input validation
class UserInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 128:
            raise ValueError("Password must be between 8 and 128 characters long.")
        return value


# Strawberry GraphQL types
@strawberry.type
class UserType:
    id: int
    email: str
    sign_in_count: int


@strawberry.type
class GlobalSignInCount:
    count: int


@strawberry.input
class RegisterInput:
    email: str
    password: str


@strawberry.type
class RegisterResponse:
    user: UserType
    access_token: str


@strawberry.input
class LoginInput:
    email: str
    password: str


@strawberry.type
class LoginResponse:
    user: UserType
    access_token: str
