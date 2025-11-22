from fastapi import APIRouter, Depends, HTTPException, status
from ..controllers.user_controller import get_user_profile, update_user_profile
from ..models.user_models import UpdateProfileRequest, UserProfileResponse
from ..dependencies import get_current_user, require_types

router = APIRouter()

@router.get(
    "/profile/me",
    summary="Xem hồ sơ cá nhân",
    response_model=UserProfileResponse,
    description="""
    Trả về thông tin chi tiết của người dùng đang đăng nhập.
    - Nếu là **STUDENT**: Kèm theo thống kê hoạt động, ngày công.
    - Nếu là **ORGANIZER**: Kèm theo số lượng sự kiện quản lý.
    """
    # responses={
    #     200: {"description": "Thành công"}
    # }
)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    result = get_user_profile(str(current_user["id"]))
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.put(
    "/profile/me",
    summary="Cập nhật hồ sơ",
    response_model=UserProfileResponse,
    description="""
    Cập nhật các thông tin cơ bản (Tên, SĐT...).
    **Yêu cầu bảo mật:** Header `X-CSRF-Token` bắt buộc phải có.
    """,
    responses={
        400: {"description": "Không có trường nào được gửi để cập nhật"},
        403: {"description": "Thiếu hoặc sai CSRF Token"}
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