
from pydantic import BaseModel, EmailStr, ConfigDict


# Data required when registering a user
class UserCreate(BaseModel):

    name: str
    email: EmailStr
    password: str


# Data returned to the client
class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Response returned after login
class TokenResponse(BaseModel):

    access_token: str
    token_type: str
