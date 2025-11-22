from pydantic import BaseModel
from typing import Literal, Optional, Union
from datetime import datetime
from uuid import UUID

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None

    type: Literal['STUDENT', 'ORGANIZER']

    student_no: Optional[str] = None
    organizer_no: Optional[str] = None
    org_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    user_id: str

class LoginResponse(BaseModel):
    token_type: str = "bearer"
    user: dict 
    csrf_token: str

class CsrfResponse(BaseModel):
    csrf_token: str

class RefreshResponse(BaseModel):
    message: str = "Access token refreshed successfully"

class MessageResponse(BaseModel):
    message: str

# ---------------------------------------
class UpdateProfileRequest(BaseModel):
    # Can add more fields as needed
    full_name: Optional[str] = None
    phone: Optional[str] = None

# 1. Model cơ bản chung cho mọi User
class BaseUserProfileResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    type: str # STUDENT, ORGANIZER
    # Đã bỏ: is_active, created_at, updated_at

    class Config:
        from_attributes = True

# 2. Model thống kê cho Student
class StudentStats(BaseModel):
    activities_joined: int = 0        
    total_social_work_days: float = 0.0 
    pending_activities: int = 0       

# 3. Model thống kê cho Organizer
class OrganizerStats(BaseModel):
    managed_events_count: int = 0     

# 4. Response đầy đủ cho Student
class StudentProfileResponse(BaseUserProfileResponse):
    student_info: Optional[dict] = None # Chứa student_no...
    stats: StudentStats

# 5. Response đầy đủ cho Organizer
class OrganizerProfileResponse(BaseUserProfileResponse):
    organizer_info: Optional[dict] = None # Chứa org_name...
    stats: OrganizerStats

# 6. Union Model: Để FastAPI tự chọn model phù hợp khi trả về
UserProfileResponse = Union[StudentProfileResponse, OrganizerProfileResponse, BaseUserProfileResponse]