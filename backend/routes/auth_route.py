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
    refresh_token = result.get("refresh_token")
    csrf_token = auth_controller.attach_csrf_token(request_obj.session)
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
            max_age=env_settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
        )
    return {
        "token_type": "bearer",
        "user": result["user"],
        "csrf_token": csrf_token
    }

@router.post("/logout")
def logout_user(request: Request, response: Response, current_user: dict = Depends(get_current_user)):
    # Perform any server-side logout work (controller-level). Keep controller lightx
    result = auth_controller.logout(request, response, current_user['id'])
    return result

@router.get("/csrf")
def get_csrf_token(request: Request, response: Response):
    csrf_token = auth_controller.attach_csrf_token(request.session)
    return {"csrf_token": csrf_token}

@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    try:
        payload = jwt.decode(refresh_token, env_settings.JWT_SECRET, algorithms=[env_settings.JWT_ALGO])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        access_token = create_access_token(data={"sub": user_id, "type": "access"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # True ở production
            samesite="lax",
            max_age=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")