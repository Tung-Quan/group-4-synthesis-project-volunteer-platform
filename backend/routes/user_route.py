from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models.user_models import *
from ..controllers.user_controller import *

router = APIRouter()

@router.get("/")
def get_profile(user_id: str):
    request = ViewProfileRequest(user_id=user_id)
    result, status_code = view_profile(request)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result["message"])
    return result