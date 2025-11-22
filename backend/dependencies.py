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
    # Assert user existence
    user = db.fetch_one_sync("SELECT * FROM users WHERE id = %s AND is_active = TRUE", (user_id,))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    # Attach roles derived from students/organizers tables
    roles = []
    if db.fetch_one_sync("SELECT 1 FROM students WHERE user_id = %s", (user_id,)):
        roles.append('STUDENT')
    if db.fetch_one_sync("SELECT 1 FROM organizers WHERE user_id = %s", (user_id,)):
        roles.append('ORGANIZER')
    user['roles'] = roles
    # provide legacy `type` for compatibility
    if len(roles) == 2:
        user['type'] = 'BOTH'
    elif len(roles) == 1:
        user['type'] = roles[0]
    else:
        user['type'] = 'NONE'
    return user

def require_roles(*roles: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user_roles = current_user.get('roles', [])
        # check if any of the user's roles match required roles
        if not any(r in user_roles for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with roles '{user_roles}' not authorized for roles: {', '.join(roles)}"
            )
        return current_user
    return role_checker

def verify_csrf(request):
    session_token = request.session.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")
    if not session_token or not header_token or session_token != header_token:
        raise HTTPException(status_code=403, detail="CSRF token missing or invalid")
    return True
