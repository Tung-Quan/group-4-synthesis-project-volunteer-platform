from pydantic import BaseModel, field_validator
from datetime import datetime, date, time
from typing import Optional

class EventResponse(BaseModel):
    id: str
    organizer_user_id: str
    title: str
    description: str
    location: str
    status: str

# Model trả về Slot (Dùng cho API lấy chi tiết slot hoặc list slot)
class SlotResponse(BaseModel):
    id: str         # Đổi từ slot_id thành id cho chuẩn chung
    event_id: str   # Thêm event_id để biết slot thuộc event nào
    work_date: date
    starts_at: time
    ends_at: time
    capacity: int
    day_reward: float

    # Hai biến mới
    approved_count: int = 0  # Số người đã được nhận (Approved)
    applied_count: int = 0   # Số người đang chờ (Applied)

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

    # VALIDATION: Đảm bảo giờ kết thúc phải sau giờ bắt đầu
    @field_validator('ends_at')
    def check_time_order(cls, v, values):
        if 'starts_at' in values.data and v <= values.data['starts_at']:
            raise ValueError('Giờ kết thúc (ends_at) phải sau giờ bắt đầu (starts_at)')
        return v
    
    # VALIDATION: Đảm bảo capacity > 0
    @field_validator('capacity')
    def check_capacity(cls, v):
        if v <= 0:
            raise ValueError('Số lượng (capacity) phải lớn hơn 0')
        return v

class SlotUpdate(BaseModel):
    work_date: Optional[date] = None
    starts_at: Optional[time] = None
    ends_at: Optional[time] = None
    capacity: Optional[int] = None
    day_reward: Optional[float] = None

    # Vẫn cần validate nếu người dùng gửi cả 2 trường start và end
    @field_validator('ends_at')
    def check_time_order(cls, v, values):
        if v is not None and 'starts_at' in values.data and values.data['starts_at'] is not None:
             if v <= values.data['starts_at']:
                raise ValueError('Giờ kết thúc phải sau giờ bắt đầu')
        return v

class UpdateEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


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

class CheckingAttendance(BaseModel):
    organizer_id: str
    applicant_id: str
    attended: bool = True

class ReviewApplication(BaseModel): 
    application_id: str
    approve: bool 
    reason: str | None = None

class CancelApplication(BaseModel): # For students cancel their applications
    event_id: str
    slot_id: str

class MessageResponse(BaseModel):
    message: str