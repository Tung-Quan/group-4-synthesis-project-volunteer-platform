from fastapi import Request, HTTPException, Depends, status
import jwt
from .config.env import env_settings
from .db.database import db

async def get_current_user(req: Request) -> dict:
    """
    take user info from token.
    """
    try:
        # 1. Take token from coookies
        token = req.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        # 2. Decode token
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
    # 3. take user info from DB
    query = """
        SELECT id, email, full_name, phone, type, is_active 
        FROM users 
        WHERE id = %s AND is_active = TRUE
    """
    user = db.fetch_one_sync(query, (user_id,))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user

def require_types(*allowed_types: str):
    async def type_checker(current_user: dict = Depends(get_current_user)):
        user_type = current_user.get('type')
        # check if any of the user's types match required types
        if user_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"type '{user_type}' is not authorized. Required: {allowed_types}"
            )
        return current_user
    return type_checker

def verify_csrf(request):
    session_token = request.session.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")
    if not session_token or not header_token or session_token != header_token:
        raise HTTPException(status_code=403, detail="CSRF token missing or invalid")
    return True
