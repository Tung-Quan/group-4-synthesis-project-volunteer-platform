from fastapi import APIRouter, HTTPException, status, Request
from ..models.user_models import RegisterRequest, LoginRequest
from ..controllers import auth_controller

router = APIRouter()

@router.post("/register")
def register_user(request: RegisterRequest):
    result = auth_controller.register(request)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.post("/login")
def login_user(request: LoginRequest):
    result = auth_controller.login(request)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@router.post("/logout")
def logout_user(request: Request):
    result = auth_controller.logout(request.headers.get("user_id"))
    return result