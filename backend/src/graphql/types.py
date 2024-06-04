import strawberry


@strawberry.type
class UserType:
    id: int
    email: str
    sign_in_count: int


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
