from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
import os
from ..config.env import env_settings
from ..models.user_models import RegisterRequest, LoginRequest, LoginResponse, MessageResponse, CsrfResponse, RefreshResponse, RegisterResponse
from ..controllers import auth_controller
from ..config.security import make_csrf
from ..dependencies import get_current_user

import jwt
from jwt import PyJWTError

router = APIRouter()


@router.post(
    "/register",
    summary="Register a new account",
    description="Create a new account for Student or Organizer type.",
    response_model=RegisterResponse,
    responses={
        400: {"description": "Missing information or Invalid Type"},
        409: {"description": "Email already registered"},
        500: {"description": "Server error or Type creation failed"}
    }
)
def register_user(request: RegisterRequest):
    result = auth_controller.register(request)
    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"], detail=result["error"])
    return result


@router.post(
    "/login",
    summary="Login to system",
    response_model=LoginResponse,
    description="""
    Login with Email/Password.\n
    - **Access/Refresh Token**: Automatically set in HttpOnly Cookies.
    - **CSRF Token**: Returned in response body. Frontend must save this for subsequent POST/PUT etc. requests.
    """,
    responses={
        401: {"description": "Invalid email or password"}
    }
)
def login_user(request: LoginRequest, response: Response, request_obj: Request):
    result = auth_controller.login(request)
    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"], detail=result["error"])
    access_token = result.get("access_token")
    refresh_token = result.get("refresh_token")
    # csrf_token = result.get("csrf_token")
    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
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
    summary="Logout",
    response_model=MessageResponse,
    description="Clear Access and Refresh Token cookies.",
)
def logout_user(request: Request, response: Response, current_user: dict = Depends(get_current_user)):
    # Perform any server-side logout work (controller-level). Keep controller lightx
    result = auth_controller.logout(request, response, current_user['id'])
    return result


@router.get(
    "/csrf",
    summary="Get CSRF Token",
    response_model=CsrfResponse,
    description="Retrieve a new CSRF Token (useful when reloading page).",
)
def get_csrf_token(request: Request, response: Response):
    csrf_token = auth_controller.regenerate_csrf_token(request.session)
    return {"csrf_token": csrf_token}


@router.post(
    "/refresh",
    summary="Refresh Access Token",
    response_model=RefreshResponse,
    description="Call this API when Access Token expires (401). Browser automatically sends Refresh Token cookie.",
    responses={
        401: {"description": "Refresh token missing or invalid"}
    }
)
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    result = auth_controller.refresh(refresh_token)

    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"], detail=result["error"])

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
