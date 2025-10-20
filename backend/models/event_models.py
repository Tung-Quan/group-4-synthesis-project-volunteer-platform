from pydantic import BaseModel

class CreateEventRequest(BaseModel):
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int
    organizer_id: str

class UpdateEventRequest(BaseModel):
    event_id: str
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int
    organizer_id: str

class ApplyEvent(BaseModel):
    event_id: str
    applicant_id: str
    name: str
    department: str
    email: str
    phone_no: str 

class CheckingAttendance(BaseModel):
    organizer_id: str
    applicant_id: str
    attended: bool = True

class ReviewApplication(BaseModel):
    organizer_id: str
    application_id: str
    approve: bool 
    reason: str | None = None