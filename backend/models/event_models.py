from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional

class EventResponse(BaseModel):
    id: str
    organizer_user_id: str
    title: str
    description: str
    location: str
    status: str

class Slot(BaseModel):
    slot_id: str
    work_date: date
    starts_at: time
    ends_at: time
    capacity: int
    day_reward: float

class EventDetail(BaseModel):
    id: str
    organizer_user_id: str
    title: str
    description: str
    location: str
    status: str
    slots: list[Slot]

class SlotCreate(BaseModel):
    work_date: date
    starts_at: time
    ends_at: time
    capacity: int
    day_reward: float

class EventRequest(BaseModel):
    title: str
    description: str
    location: str
    slots: list[SlotCreate]

class UpdateEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


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