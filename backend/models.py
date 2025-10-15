from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str
    email: str
    display_name: Optional[str]
    type: Optional[str] = "BOTH"
    is_active: bool = True
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Event(BaseModel):
    id: str
    created_by: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    capacity: Optional[int] = 1
    status: Optional[str] = "OPEN"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Application(BaseModel):
    id: str
    event_id: str
    applicant_id: str
    status: Optional[str] = "PENDING"
    note: Optional[str] = None
    reason: Optional[str] = None
    created_at: Optional[datetime] = None
