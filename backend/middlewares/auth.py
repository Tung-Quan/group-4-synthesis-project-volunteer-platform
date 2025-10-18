from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from typing import Callable
from fastapi import Request
from ..config.security import make_csrf, assert_csrf
from ..config.env import env_settings
from ..config.logger import logger
import jwt

PROTECTED_PREFIXES = ("/", "/dashboard", "/settings")  
EXCLUDE_PATHS = {"/auth/login","/auth/register", "/auth/refresh", "/healthz", "/static", "/favicon.ico"}

class PageAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path
        if any(path.startswith(prefix) for prefix in EXCLUDE_PATHS):
            return await call_next(request) 
        
        # if any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
        #     token = request.cookies.get("access_token")
        #     if not token:
        #         return PlainTextResponse("Unauthorized", status_code=401)
        #     # try:
        #     #     decode_token(token, expected_type="access")
        #     # except JWTError:
        #     try:
        #         jwt.decode(token, env_settings.JWT_SECRET, algorithms=[env_settings.JWT_ALGO])
        #     except jwt.PyJWTError:
        #         return PlainTextResponse("Unauthorized", status_code=401)
        
        # 2. Nếu đường dẫn KHÔNG CÔNG KHAI, nó mặc định là ĐƯỢC BẢO VỆ
        #    Tiến hành kiểm tra token
        token = request.cookies.get("access_token")
        if not token:
            return PlainTextResponse("Unauthorized", status_code=401)
        
        try:
            jwt.decode(token, env_settings.JWT_SECRET, algorithms=[env_settings.JWT_ALGO])
        except jwt.PyJWTError:
            return PlainTextResponse("Unauthorized", status_code=401)

        response = await call_next(request)
        logger.info(f"Request: {request.method} {request.url} - Response: {response.status_code}")
        return response

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bỏ qua CSRF cho các đường dẫn được loại trừ
        path = request.url.path
        if any(path.startswith(prefix) for prefix in EXCLUDE_PATHS):
            return await call_next(request)
        
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = make_csrf()
        

        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            assert_csrf(request)

        response = await call_next(request)
        return response