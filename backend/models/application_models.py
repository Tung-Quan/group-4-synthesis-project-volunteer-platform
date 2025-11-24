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

class CancelApplication(BaseModel): # For students cancel their applications
    slot_id: str
 