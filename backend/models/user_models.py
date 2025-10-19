from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str
    type: Literal['STUDENT', 'ORGANIZER']

class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    user_id: str

class UpdateProfileRequest(BaseModel):
    display_name: str | None = None

class UserProfileResponse(BaseModel):
    id: str
    email: str
    display_name: str
    type: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True