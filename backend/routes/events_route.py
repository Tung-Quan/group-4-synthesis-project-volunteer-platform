from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models.event_models import CreateEventRequest, UpdateEventRequest
from ..controllers.event_controller import events, create_event, update_event

router = APIRouter()

@router.get("/")
def get_events(request: Request):
    result, status_code = events(request)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.post("/")
def post_event(request: CreateEventRequest):
    result, status_code = create_event(request)
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result

@router.put("/")
def put_event(request: UpdateEventRequest, req: Request):
    result, status_code = update_event(request, req)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result