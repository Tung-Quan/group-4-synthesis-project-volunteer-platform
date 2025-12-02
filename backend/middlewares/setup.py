from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
# from .auth import PageAuthMiddleware, CSRFMiddleware
from .auth import CSRFMiddleware
from ..config.env import env_settings
from ..config.logger import logger
from datetime import datetime


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        # try:
        #     # Try to read body for debug (may be empty or streamed)
        #     body = await request.body()
        #     if body:
        #         try:
        #             logger.debug(f"Request body: {body.decode('utf-8')}")
        #         except Exception:
        #             logger.debug(f"Request body (raw bytes, {len(body)} bytes)")
        # except Exception:
        #     # If the body cannot be read (e.g., streaming) just continue
        #     logger.debug("Could not read request body")
        start = datetime.utcnow()
        try:
            response = await call_next(request)
            response.headers.update({
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
                "X-Frame-Options": "DENY",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "no-referrer",
                "Permissions-Policy": "geolocation=(), microphone=()",
            })
        except Exception:
            # Log exception with full stacktrace then re-raise so exception handlers still run
            logger.exception("Unhandled exception while handling request")
            raise
        duration = (datetime.utcnow() - start).total_seconds()
        logger.info(
            f"Completed {request.method} {request.url} -> {response.status_code} in {duration:.3f}s")
        return response


def setup_middlewares(app: FastAPI):
    """Register middlewares in a predictable order. SessionMiddleware must be added
    before any middleware that accesses request.session (CSRFMiddleware depends on it).
    """
    # CORS can be added first
    origins = ["http://localhost:5173"]
    if env_settings.API_ORIGIN:
        origins.append(env_settings.API_ORIGIN)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],
    )
    logger.info("CORSMiddleware added.")
    # Add custom middlewares that rely on sessions or authentication
    app.add_middleware(CSRFMiddleware)
    logger.info("CSRFMiddleware added.")
    # IMPORTANT: SessionMiddleware must be installed before any middleware that accesses
    # request.session at runtime. Because Starlette's add_middleware builds the stack
    # such that the last added middleware is executed first, we add SessionMiddleware
    # after CSRFMiddleware so its runtime execution precedes CSRFMiddleware.
    app.add_middleware(SessionMiddleware, secret_key=env_settings.JWT_SECRET)
    logger.info("SessionMiddleware added.")
    # Security headers as a middleware added last so it can update the response
    app.add_middleware(SecurityHeadersMiddleware)
    logger.info("SecurityHeadersMiddleware added.")
