from fastapi import APIRouter, Depends, HTTPException, status
from ..controllers.user_controller import get_user_profile, update_user_profile
from ..models.user_models import UpdateProfileRequest, UserProfileResponse
from ..dependencies import get_current_user, require_roles

router = APIRouter()
@router.get("/profile/me", response_model=UserProfileResponse)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    result = get_user_profile(str(current_user["id"]))
    if "error" in result:
        raise HTTPException(status_code=current_user["status_code"], detail=current_user["error"])
    return result

@router.put("/profile/me", response_model=UserProfileResponse)
def update_my_profile(
    request: UpdateProfileRequest, 
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["id"])
    result = update_user_profile(user_id, request)

    if "error" in result:
        raise HTTPException(status_code=current_user["status_code"], detail=current_user["error"])
    return result