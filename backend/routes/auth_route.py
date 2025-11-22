from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
import os
from ..config.env import env_settings
from ..models.user_models import RegisterRequest, LoginRequest, LoginResponse, MessageResponse, CsrfResponse, RefreshResponse
from ..controllers import auth_controller
from ..config.security import make_csrf
from ..dependencies import get_current_user

import jwt
from jwt import PyJWTError

router = APIRouter()

@router.post(
    "/register",
    summary="Đăng ký tài khoản mới",
    description="Tạo tài khoản cho Student hoặc Organizer. Trả về thông tin user nếu thành công.",
    response_model=dict, # Hoặc UserProfileResponse nếu controller trả về đúng format
    responses={
        400: {"description": "Thiếu thông tin hoặc Role không hợp lệ"},
        409: {"description": "Email đã tồn tại"},
        500: {"description": "Lỗi server hoặc lỗi tạo dữ liệu role"}
    }
)
def register_user(request: RegisterRequest):
    """
    - **email**: Email duy nhất
    - **password**: Mật khẩu
    - **type**: 'STUDENT' hoặc 'ORGANIZER'
    - **student_no / organizer_no**: Bắt buộc tương ứng với role
    """
    result = auth_controller.register(request)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.post(
    "/login",
    summary="Đăng nhập hệ thống",
    response_model=LoginResponse,
    description="""
    Đăng nhập bằng Email/Pass. 
    - **Access/Refresh Token**: Được set tự động vào HttpOnly Cookie.
    - **CSRF Token**: Trả về trong body, Frontend cần lưu lại để dùng cho các request POST/PUT sau này.
    """,
    responses={
        401: {"description": "Sai email hoặc mật khẩu"}
    }
)
def login_user(request: LoginRequest, response: Response,request_obj: Request):
    result = auth_controller.login(request)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    access_token = result.get("access_token")
    refresh_token = result.get("refresh_token")
    # csrf_token = result.get("csrf_token")
    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False, # Set to True in production with HTTPS
            samesite="lax",
            max_age=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # True ở production
            samesite="lax",
            path="/auth/refresh",
            max_age=env_settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
        )
    csrf_token = auth_controller.regenerate_csrf_token(request_obj.session)
    return {
        "token_type": "bearer",
        "user": result["user"],
        "csrf_token": csrf_token
    }

@router.post(
    "/logout",
    summary="Đăng xuất",
    response_model=MessageResponse,
    description="Xóa toàn bộ Cookie Access và Refresh Token.",
)
def logout_user(request: Request, response: Response, current_user: dict = Depends(get_current_user)):
    # Perform any server-side logout work (controller-level). Keep controller lightx
    result = auth_controller.logout(request, response, current_user['id'])
    return result

@router.get(
    "/csrf",
    summary="Lấy CSRF Token",
    response_model=CsrfResponse,
    description="Dùng để lấy lại CSRF Token khi người dùng reload trang (F5) mà vẫn còn phiên đăng nhập (Cookie).",
)
def get_csrf_token(request: Request, response: Response):
    csrf_token = auth_controller.regenerate_csrf_token(request.session)
    return {"csrf_token": csrf_token}

@router.post(
    "/refresh",
    summary="Làm mới Access Token",
    response_model=RefreshResponse,
    description="Gọi API này khi Access Token hết hạn (401). Browser sẽ tự gửi Cookie Refresh Token.",
    responses={
        401: {"description": "Refresh token thiếu hoặc không hợp lệ"}
    }
)
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    result = auth_controller.refresh(refresh_token)

    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])

    new_access_token = result["access_token"]

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,  # True ở production
        samesite="lax",
        max_age=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {"message": "Access token refreshed successfully"}