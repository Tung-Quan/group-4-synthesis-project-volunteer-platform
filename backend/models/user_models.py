from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    # Optional role: if provided, controllers may create role-specific rows
    role: Literal['STUDENT', 'ORGANIZER']

    student_no: Optional[str] = None
    organizer_no: Optional[str] = None
    org_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class LogoutRequest(BaseModel):
    user_id: str


class UpdateProfileRequest(BaseModel):
    # Can add more fields as needed
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attribute = True