from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventResponse(BaseModel):
    id: str
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    location: str
    capacity: int

class CreateEventRequest(BaseModel):
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int

class UpdateEventRequest(BaseModel):
    event_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    starts_at: Optional[str] = None  # ISO 8601 format
    ends_at: Optional[str] = None    # ISO 8601 format
    capacity: Optional[int] = None

class ApplyEvent(BaseModel):
    event_id: str
    # applicant_id: str
    name: str
    department: str
    email: str
    phone_no: str 

class CheckingAttendance(BaseModel):
    organizer_id: str
    applicant_id: str
    attended: bool = True

class ReviewApplication(BaseModel): 
    application_id: str
    approve: bool 
    reason: str | None = None

class CancelApplication(BaseModel): # For students cancel their applications
    application_id: str