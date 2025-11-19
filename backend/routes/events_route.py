from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models.event_models import *
from ..controllers.event_controller import *
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=list[EventResponse])
def get_events():
    result = events()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.get("/{id}", response_model=EventResponse)
def get_event_by_id(id: str):
    result = event_id(id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.post("/")
def post_event(request: CreateEventRequest, current_user: dict = Depends(get_current_user)):
    result = create_event(request, str(current_user["id"]))
    if  result is None:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY)
    return result

@router.post("/")
def create_event_route(request: CreateEventRequest, current_user: dict = Depends(get_current_user)):
    if current_user["type"] not in ("BOTH", "ORGANIZER"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    result = create_event(request, str(current_user["id"]))
    if result is None:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY)
    return result


@router.patch("/")
def update_event_route(request: UpdateEventRequest, current_user: dict = Depends(get_current_user)):
    result, status_code = update_event(request, str(current_user["id"]))
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.post("/apply")
def apply_even_route(request: ApplyEvent, current_user: dict = Depends(get_current_user)):
    result, status_code = apply_event(request, str(current_user["id"]))
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.post("/attendance")
def check_attendance_route(request: CheckingAttendance):
    result, status_code = check_attendance(request)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.post("/review")
def review_app(request: ReviewApplication, current_user: dict = Depends(get_current_user)):
    result, status_code = review_application(request, str(current_user["id"]))
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.post("/cancel")
def cancel_application_route(
    request: CancelApplication,
    current_user: dict = Depends(get_current_user)
):
    result, code = cancel_application(request, str(current_user["id"]))
    if code != 200:
        raise HTTPException(code, result["message"])
    return result
