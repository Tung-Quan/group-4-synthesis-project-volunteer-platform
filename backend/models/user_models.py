from pydantic import BaseModel
from typing import Optional

class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str
    type: str = "BOTH"

class LoginRequest(BaseModel):
    email: str
    password: str
