from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    role: str | None = "user"

class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str 

class UserCreateResponse(BaseModel):
    user_id: UUID
    message: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str