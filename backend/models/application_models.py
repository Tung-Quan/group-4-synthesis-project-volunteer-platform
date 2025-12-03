from pydantic import BaseModel, field_validator
from datetime import datetime, date, time
from typing import Optional


class ApplyEvent(BaseModel):
    event_id: str
    slot_id: str
    note: str


class UpdateAttendance(BaseModel):
    slot_id: str
    student_user_id: str
    attended: bool


class ReviewApplication(BaseModel):
    slot_id: str
    student_user_id: str
    approve: bool
    reason: Optional[str] = None


class CancelApplication(BaseModel):  # For students cancel their applications
    slot_id: str


class UserApplication(BaseModel):
    event_id: str
    slot_id: str
    event_name: str
    work_date: date
    starts_at: time
    ends_at: time
    location: str
    status: str


class ApplicationDetail(BaseModel):
    event_id: str
    event_name: str
    org_name: str
    description: str
    work_date: date
    starts_at: time
    ends_at: time
    location: str
    day_reward: float
    status: str

class ApplicationResponse(BaseModel):
    student_user_id: str
    student_name: str
    student_no: str
    note: str
    status: str
