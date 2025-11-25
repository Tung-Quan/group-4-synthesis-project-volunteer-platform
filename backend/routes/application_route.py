from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models import application_models
from ..controllers import application_controller
from ..dependencies import get_current_user, require_types

router = APIRouter()

@router.post("/apply")
def apply_event(
    request: application_models.ApplyEvent, 
    current_user: dict = Depends(require_types("STUDENT"))
):
    result, status_code = application_controller.apply_event(request, str(current_user["id"]))
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.patch("/{event_id}/attendance")
def attendance(
    event_id: str, 
    request: application_models.UpdateAttendance, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    result, code = application_controller.mark_attendance(event_id, request, str(current_user["id"]))
    if code != 200:
        raise HTTPException(code, result["message"])
    return result


@router.patch("/{event_id}/review")
def review_app(
    event_id: str, 
    request: application_models.ReviewApplication, 
    current_user: dict = Depends(require_types("ORGANIZER"))
):
    result, status_code = application_controller.review_application(event_id, request, str(current_user["id"]))
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.patch("/{event_id}/cancel", status_code=200)
def cancel_application_route(
    event_id: str, 
    request: application_models.CancelApplication, 
    current_user: dict = Depends(require_types("STUDENT"))
):
    result, code = application_controller.cancel_application(event_id, request, str(current_user["id"]))
    if code != 200:
        raise HTTPException(status_code=code, detail=result["message"])

    return result

