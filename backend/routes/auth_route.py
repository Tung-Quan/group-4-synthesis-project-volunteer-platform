from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
import os
from ..config.env import env_settings
from ..models.user_models import RegisterRequest, LoginRequest
from ..controllers import auth_controller
from ..config.security import make_csrf
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/register")
def register_user(request: RegisterRequest):
    result = auth_controller.register(request)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.post("/login")
def login_user(request: LoginRequest, response: Response,request_obj: Request):
    result = auth_controller.login(request)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    access_token = result.get("access_token")
    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False, # Set to True in production with HTTPS
            samesite="strict",
            max_age=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    # Attach CSRF token to session
    csrf_token = auth_controller.attach_csrf_token(request_obj.session)
    response.set_cookie(
        key="csrf_token", 
        value=csrf_token, 
        httponly=True, 
        secure=False, 
        samesite="strict",
        max_age=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    result["csrf_token"] = csrf_token
    return result

@router.post("/logout")
def logout_user(request: Request, response: Response, current_user: dict = Depends(get_current_user)):
    # Perform any server-side logout work (controller-level). Keep controller lightx
    result = auth_controller.logout(request, response, current_user['id'])
    return result

@router.get("/csrf")
def get_csrf_token(request: Request, response: Response):
    csrf_token = auth_controller.attach_csrf_token(request.session)
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=True,
        secure=False,  # Localhost
        samesite="strict",
        max_age=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"csrf_token": csrf_token}