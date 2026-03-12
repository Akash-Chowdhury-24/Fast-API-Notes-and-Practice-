from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar("T")


class UserCreateModel(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"


class LoginModel(BaseModel):
    email: str
    password: str


class UserResponseModel(BaseModel):
    id: str
    name: str
    email: str
    role: str = "user"

class UserAuthTokenResponseModel(BaseModel):
    user: UserResponseModel
    access_token: str

class APIResponseModel(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T