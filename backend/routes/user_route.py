from fastapi import APIRouter, Depends, HTTPException, status
from ..controllers.user_controller import get_user_profile, update_user_profile
from ..models.user_models import UpdateProfileRequest, UserProfileResponse
from ..dependencies import get_current_user, require_types

router = APIRouter()

@router.get(
    "/profile/me",
    summary="Get Current User Profile",
    response_model=UserProfileResponse,
    description="""
    Retrieve detailed profile of the currently logged-in user.\n
    - **STUDENT**: Includes activity stats and social work days.
    - **ORGANIZER**: Includes managed events count.
    """
)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    result = get_user_profile(str(current_user["id"]))
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.put(
    "/profile/me",
    summary="Update User Profile",
    response_model=UserProfileResponse,
    description="""
    Update basic profile information (Full Name, Phone).
    **Security Requirement:** `X-CSRF-Token` header is required.
    """,
    responses={
        400: {"description": "No fields provided for update"},
        403: {"description": "Missing or invalid CSRF Token"},
        500: {"description": "Failed to update profile"}
    }
)
def update_my_profile(
    request: UpdateProfileRequest, 
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["id"])
    result = update_user_profile(user_id, request)

    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result