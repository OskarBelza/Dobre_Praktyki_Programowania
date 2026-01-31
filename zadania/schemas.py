from pydantic import BaseModel
from typing import List


class UserSchema(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str
    roles: str = "ROLE_USER"


class Token(BaseModel):
    access_token: str
    token_type: str


class UserDetails(BaseModel):
    user_id: int
    roles: List[str]
    exp: int
