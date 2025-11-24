from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models import event_models
from ..controllers import event_controller
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=list[event_models.EventResponse], status_code=status.HTTP_200_OK)
def get_events():
    result = event_controller.get_events()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.get("/{id}", response_model=event_models.EventDetail, status_code=status.HTTP_200_OK)
def get_event_by_id(id: str):
    result = event_controller.get_event_by_id(id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(request: event_models.EventRequest, current_user: dict = Depends(get_current_user)):
    results = event_controller.create_event(request, str(current_user["id"]))
    if results is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return results

@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_event_info(id: str, request: event_models.UpdateEvent, current_user: dict = Depends(get_current_user)):
    result = event_controller.update_event_info(id, request, str(current_user["id"]))
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return result

@router.post("/apply")
def apply_event(request: event_models.ApplyEvent, current_user: dict = Depends(get_current_user)):
    result, status_code = event_controller.apply_event(request, str(current_user["id"]))
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.patch("/{event_id}/attendance")
def attendance(event_id: str, request: event_models.UpdateAttendance, current_user: dict = Depends(get_current_user)):
    result, code = event_controller.mark_attendance(event_id, request, str(current_user["id"]))
    if code != 200:
        raise HTTPException(code, result["message"])
    return result


@router.patch("/{event_id}/review")
def review_app(event_id: str, request: event_models.ReviewApplication, current_user: dict = Depends(get_current_user)):
    result, status_code = event_controller.review_application(event_id, request, str(current_user["id"]))
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.patch("/{event_id}/cancel", status_code=200)
def cancel_application_route(event_id: str, request: event_models.CancelApplication, current_user: dict = Depends(get_current_user)):
    result, code = event_controller.cancel_application(event_id, request, str(current_user["id"]))
    if code != 200:
        raise HTTPException(status_code=code, detail=result["message"])

    return result
