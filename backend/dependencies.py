from fastapi import Request, HTTPException, Depends, status
import jwt
from .config.env import env_settings
from .db.database import db

async def get_current_user(req: Request) -> dict:
    try :
        token = req.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
        payload = jwt.decode(token, env_settings.JWT_SECRET, algorithms=[env_settings.JWT_ALGO])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        # 
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    user = db.fetch_one_sync("SELECT * FROM users WHERE id = %s AND is_active = TRUE", (user_id,))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    
    return user

# def require_roles(*roles: str):
#     async def role_checker(current_user: dict = Depends(get_current_user)):
#         user_type = current_user.get('type')
#         if user_type not in roles or not both:
#             raise HTTPException(403, "Insufficient role")
#         return u
#     return dep
def require_roles(*roles: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user_type = current_user.get('type')
        # check if user_type is in roles
        if user_type not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="User with roles '{user_type}' not authorized for roles: {roles}'"
            )
        return current_user
    return role_checker

def assert_csrf(request):
    session_token = request.session.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")
    if not session_token or not header_token or session_token != header_token:
        raise HTTPException(status_code=403, detail="CSRF token missing or invalid")
    return True
