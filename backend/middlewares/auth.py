from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.responses import PlainTextResponse
from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from ..config.security import make_csrf
from ..dependencies import verify_csrf
from ..config.env import env_settings
from ..config.logger import logger
import jwt

PROTECTED_PREFIXES = ("/", "/dashboard", "/settings")  
EXCLUDE_PATHS = {
                "/auth/login","/auth/register", "/auth/refresh", 
                 "/healthz", "/static", "/favicon.ico"
                #  ,"/users/profile/me"
                # ,"auth/logout"
                 }

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bỏ qua CSRF cho các đường dẫn được loại trừ
        path = request.url.path
        if any(path.startswith(prefix) for prefix in EXCLUDE_PATHS):
            return await call_next(request)
        
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = make_csrf()

        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            try:
                verify_csrf(request)
            except HTTPException as e:
                # Return a proper 403 JSON response when CSRF validation fails
                logger.warning(f"CSRF validation failed for {request.url.path}: {getattr(e, 'detail', None)}")
                return JSONResponse(status_code=e.status_code, content={"detail": getattr(e, 'detail', 'CSRF token missing or invalid at CSRFMiddleware')})
            except Exception:
                # Unexpected error in CSRF check -> log and return 500
                logger.exception("Unexpected error during CSRF validation")
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})

        response = await call_next(request)
        return response