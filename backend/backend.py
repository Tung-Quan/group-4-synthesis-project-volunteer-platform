# import fastapi 
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import psycopg2
# import os,time, uuid, secrets
# import logging
# import bcrypt
# import threading

# from typing import Optional

# from fastapi import FastAPI,HTTPException,security, Depends, Request,status, APIRouter
# from fastapi.responses import ORJSONResponse, PlainTextResponse
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.middleware.trustedhost import TrustedHostMiddleware
# from models import User, Event, Application
# from pydantic import BaseModel, Field
# from fastapi import Request, Response
# from typing import Callable
# from security_cookies import create_access_token, create_refresh_token, get_current_user, require_roles

# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded

# from datetime import datetime, timedelta


# from dotenv import load_dotenv,dotenv_values
# load_dotenv()
# # Use python-jose for JWT handling (installed as python-jose)
# from datetime import datetime, timedelta
# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException, status
# # check connect
# # print("DB_HOST:", os.getenv("DATABASE_HOST")) 

# # Set up logging as [ Date-Time ]  [ Level ]  [ Module ]  Message
# LOG_FORMAT = "[ %(asctime)s ]  [ %(levelname)s ]  %(message)s"
# logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
# logger = logging.getLogger(__name__)


# class ENV:
#     #read .env in the root directory
#     #load .env variables into ENV class attributes
#     #for example, ENV.DB_HOST = os.getenv("DB_HOST")
    
#     def __init__(self):
#         # Read .env values first, then fall back to environment variables.
#         self.DATABASE_USER = os.getenv("DATABASE_USER")
#         self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
#         self.DATABASE_HOST = os.getenv("DATABASE_HOST")
#         self.DATABASE_NAME = os.getenv("DATABASE_NAME")
#         self.PORT = os.getenv("PORT", 8000)
#         self.JWT_SECRET = os.getenv("JWT_SECRET", "super-long-random-string")
#         self.JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
#         self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
#         self.REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "7"))
#         self.COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")  
#         self.BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
#         self.API_ORIGIN = os.getenv("API_ORIGIN") 
#         self.ALLOWED_HOSTS = (os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")).split(",")

    
#     PORT = int(os.getenv("PORT", "8000"))
#     def get_db_url(self) -> str:
#         # Use the attribute names initialized in __init__
#         return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}/{self.DATABASE_NAME}?sslmode=require&channel_binding=require"
    
#     def get_port(self):
#         return int(self.PORT)

#     # JWT CONFIG 
#     def get_jwt_secret(self):
#         # Prefer explicit env vars; default algorithm to HS256 for safety.
#         jwt_secret = os.getenv("JWT_SECRET")
#         # some setups use JWT_ALGO, others JWT_ALGORITHM — support both
#         jwt_algo = os.getenv("JWT_ALGO")
#         # normalize algorithm value
#         if isinstance(jwt_algo, str):
#             jwt_algo = jwt_algo.strip()
#         access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
#         refresh_token_expire_minutes = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 43200))  # 30 days
#         oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
#         return jwt_secret, jwt_algo, access_token_expire_minutes, refresh_token_expire_minutes, oauth2_scheme;
# env_settings = ENV()

# #==========================SECURTY=============================================================

# _pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
# #=======================
# #-JWT and Auth settings
# #=======================
# def hash_password(password: str) -> str:
#     """Hash a password for storing."""
#     return _pwd.hash(password, rounds=env_settings.BCRYPT_ROUNDS)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a stored password against one provided by user"""
#     return _pwd.verify(plain_password, hashed_password)

# def make_jwt_token(sub: str, ttype:str, ttl: timedelta) -> str:
#     to_encode = {"sub": sub, "type": ttype, "exp": datetime.now() + ttl, "iat": datetime.now()}
#     encoded_jwt = jwt.encode(to_encode, env_settings.JWT_SECRET, algorithm=env_settings.JWT_ALGO)
#     return encoded_jwt

# #=======================
# #-Token data model
# #=======================
# PROTECTED_PREFIXES = ("/", "/dashboard", "/settings")  
# EXCLUDE_PATHS = {"/login", "/auth/login", "/auth/refresh", "/healthz", "/static", "/favicon.ico"}

# class TokenData(BaseModel):
#     sub: Optional[str] = None
#     type: Optional[str] = "access"
#     iat: int
#     exp: int
#     aud: str | None = None
#     jit: str | None = None

# def decode_token(token: str, expected_type: str = "access") -> TokenData:
#     try:
#         payload = jwt.decode(
#             token, env_settings.JWT_SECRET, 
#             algorithms=[env_settings.JWT_ALGO],
#             options={"required_exp": True, "required_iat": True}
#             )
#         sub: str = payload.get("sub")
#         ttype: str = payload.get("type")
#         if sub is None or ttype != expected_type:
#             raise JWTError()
#         return TokenData(sub=sub, type=ttype)
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")


# def make_csrf() -> str:
#     return secrets.token_urlsafe(32)

# def assert_csrf(request: Request):
#     session_token = request.session.get("csrf_token")
#     header_token = request.headers.get("X-CSRF-Token")
#     if not session_token or not header_token or session_token != header_token:
#         raise HTTPException(status_code=403, detail="CSRF token missing or invalid")
#     return True

# class PageAuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next: Callable):
#         path = request.url.path
#         if any(path.startswith(prefix) for prefix in EXCLUDE_PATHS):
#             return await call_next(request) 
    
#         if any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
#             token = request.cookies.get("access_token")
#             if not token:
#                 return PlainTextResponse("Unauthorized", status_code=401)
#             try:
#                 decode_token(token, expected_type="access")
#             except JWTError:
#                 return PlainTextResponse("Unauthorized", status_code=401)
        
#         response = await call_next(request)
#         logger.info(f"Request: {request.method} {request.url} - Response: {response.status_code}")
#         return response
    
# async def current_user(req: Request):
#     """Resolve the current user from the access_token cookie.

#     Returns a lightweight object with `.role` attribute for compatibility
#     with `require_roles`.
#     """
#     tok = req.cookies.get("access_token")
#     if not tok:
#         raise HTTPException(status_code=401, detail="Missing token")
#     data = decode_token(tok)
#     # decode_token raises an HTTPException on failure
#     if isinstance(data, HTTPException):
#         raise data
#     if data.type != "access":
#         raise HTTPException(status_code=401, detail="Wrong token type")

#     # Fetch user from DB (synchronous helper). This will block briefly during import/runtime
#     user_row = db.fetch_one_sync(
#         "SELECT id, email, display_name, type AS role, is_active FROM users WHERE id = %s",
#         (data.sub,)
#     )
#     if not user_row:
#         raise HTTPException(status_code=401, detail="User not found")

#     # Build a small object with attribute access expected by callers
#     class SimpleUser:
#         pass

#     u = SimpleUser()
#     u.id = user_row.get("id")
#     u.email = user_row.get("email")
#     u.role = user_row.get("role") or user_row.get("type")
#     u.is_active = user_row.get("is_active", True)
#     return u

# def require_roles(*roles: str):
#     async def dep(u: User = Depends(current_user)):
#         # support both attribute and dict-like users
#         role = getattr(u, "role", None) or (u.get("role") if isinstance(u, dict) else None)
#         if role not in roles:
#             raise HTTPException(status_code=403, detail="Insufficient role")
#         return u
#     return dep

# # PageAuthMiddleware should be added to the FastAPI app by calling
# # `app.add_middleware(PageAuthMiddleware)` after `app` is created. Do not
# # instantiate BaseHTTPMiddleware directly without the app argument.


# #===============================================DATABASE========================================
# # initialize database connection and use instance pattern for this class
# class DataBase:
#     """Thread-safe singleton that holds a persistent psycopg2 connection.

#     Notes:
#     - __new__ ensures only one instance is created.
#     - __init__ is guarded by _initialized so initialization happens once.
#     - Do not use a `with psycopg2.connect(...) as conn:` here because that
#       closes the connection at the end of the with-block; we want a
#       persistent connection stored on the instance.
#     """

#     _instance = None
#     _instance_lock = threading.Lock()

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             with cls._instance_lock:
#                 if cls._instance is None:
#                     cls._instance = super(DataBase, cls).__new__(cls)
#         return cls._instance

#     def __init__(self):
#         # run initialization only once
#         if getattr(self, "_initialized", False):
#             return
#         self.env = ENV()
#         # If any DB config is missing, skip making a connection at import time.
#         required = (self.env.DATABASE_HOST, self.env.DATABASE_USER, self.env.DATABASE_PASSWORD, self.env.DATABASE_NAME)
#         if not all(required):
#             logger.warning("Database environment not fully configured; skipping DB connection (import-time).")
#             self.connection = None
#             self.cursor = None
#             self._initialized = True
#             return

#         try:
#             # keep connection open on the instance (don't use `with`)
#             self.connection = psycopg2.connect(self.env.get_db_url())
#             self.cursor = self.connection.cursor()
#             logger.info("Database connected successfully")
            
            
#             #CREATE DATABASE ENUMS
#             self.cursor.execute(
#         """
#         DO $$ BEGIN 
#             IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type') THEN
#                 CREATE TYPE user_type AS ENUM ('STUDENT', 'ORGANIZER', 'BOTH');
#             END IF;
#             IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_status') THEN
#                 CREATE TYPE event_status AS ENUM ('OPEN', 'CLOSED', 'ARCHIVED');
#             END IF;
#             IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'app_status') THEN
#                 CREATE TYPE app_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED');
#             END IF;
#         END $$;
#         """
#             )
#             logger.info("Enums ensured")
            
#             #CREATE TABLES users IF NOT EXISTS
#             self.cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS users (
#             id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             email         text NOT NULL UNIQUE,
#             password_hash text NOT NULL,
#             display_name  text NOT NULL,
#             type          user_type NOT NULL DEFAULT 'BOTH',
#             is_active     boolean NOT NULL DEFAULT true,
#             created_at    timestamptz NOT NULL DEFAULT now(),
#             updated_at    timestamptz NOT NULL DEFAULT now()
#         );
#         """
#             )
            
            
#             #CREATE TABLES events IF NOT EXISTS
#             self.cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS events (
#             id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             created_by  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             title       text NOT NULL,
#             description text,
#             location    text,
#             starts_at   timestamptz,
#             ends_at     timestamptz,
#             capacity    integer NOT NULL DEFAULT 1 CHECK (capacity >= 1),
#             status      event_status NOT NULL DEFAULT 'OPEN',
#             created_at  timestamptz NOT NULL DEFAULT now(),
#             updated_at  timestamptz NOT NULL DEFAULT now(),
#             CHECK (ends_at IS NULL OR starts_at IS NULL OR ends_at >= starts_at)
#         );
#         CREATE INDEX IF NOT EXISTS idx_events_creator ON events(created_by);
#         CREATE INDEX IF NOT EXISTS idx_events_time    ON events(starts_at, ends_at);
#         CREATE INDEX IF NOT EXISTS idx_events_status  ON events(status);
#         """
#             )
            
#             #CREATE TABLES applications IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS applications (
#             id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             event_id     uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             applicant_id uuid NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
#             status       app_status NOT NULL DEFAULT 'PENDING',
#             note         text,
#             reason       text,
#             decided_at   timestamptz,
#             decided_by   uuid REFERENCES users(id),
#             created_at   timestamptz NOT NULL DEFAULT now(),
#             CONSTRAINT uq_application UNIQUE (event_id, applicant_id)
#         );
#         CREATE INDEX IF NOT EXISTS idx_app_event      ON applications(event_id);
#         CREATE INDEX IF NOT EXISTS idx_app_applicant  ON applications(applicant_id);
#         CREATE INDEX IF NOT EXISTS idx_app_status     ON applications(status);
#         """
#             )
            
#             #CREATE TABLES tags IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS tags (
#             id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             name text NOT NULL UNIQUE
#         );
#         """
#             )
            
#             #CREATE TABLES event_tags IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS event_tags (
#             event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             tag_id   uuid NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
#             CONSTRAINT pk_event_tags PRIMARY KEY (event_id, tag_id)
#         );
#         CREATE INDEX IF NOT EXISTS idx_event_tags_event ON event_tags(event_id);
#         CREATE INDEX IF NOT EXISTS idx_event_tags_tag   ON event_tags(tag_id);
#         """ 
#             )
            
            
#             #CREATE TABLES event_slots IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS event_slots (
#             id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             event_id  uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             starts_at timestamptz NOT NULL,
#             ends_at   timestamptz NOT NULL,
#             capacity  integer,
#             CONSTRAINT chk_slot_time CHECK (ends_at >= starts_at),
#             CONSTRAINT chk_slot_capacity CHECK (capacity IS NULL OR capacity >= 1)
#         );
#         CREATE INDEX IF NOT EXISTS idx_event_slots_event ON event_slots(event_id);
#         CREATE INDEX IF NOT EXISTS idx_event_slots_time  ON event_slots(starts_at, ends_at);
#         """
#             )
            
#             #CREATE TABLES saved_events IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS saved_events (
#             user_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             saved_at timestamptz NOT NULL DEFAULT now(),
#             CONSTRAINT pk_saved_events PRIMARY KEY (user_id, event_id)
#         );
#         """
#             )
            
#             #CREATE TABLE notifications IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS notifications (
#             id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             user_id    uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             type       text NOT NULL,    -- 'APP_APPROVED' | 'APP_REJECTED' | 'SYSTEM' ...
#             payload    jsonb,
#             is_read    boolean NOT NULL DEFAULT false,
#             created_at timestamptz NOT NULL DEFAULT now()
#         );
#         CREATE INDEX IF NOT EXISTS idx_notifications_user    ON notifications(user_id);
#         CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
#         """
#             )
            
#             #CREATE TABLE audit_logs IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS audit_log (
#             id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             actor_id    uuid REFERENCES users(id) ON DELETE SET NULL,
#             action      text NOT NULL,           -- 'CREATE_EVENT', 'UPDATE_EVENT', 'APPROVE', 'REJECT', ...
#             entity_type text NOT NULL,           -- 'EVENT' | 'APPLICATION' | 'USER'
#             entity_id   uuid NOT NULL,
#             meta        jsonb,
#             at          timestamptz NOT NULL DEFAULT now()
#         );
#         CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_log(actor_id);
#         CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);

#         """
#             )
            
#             #CREATE TABLE reports IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS reports (
#             id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             reporter_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             target_type  text NOT NULL,          -- 'USER' | 'EVENT' | 'APPLICATION'
#             target_id    uuid NOT NULL,
#             reason       text NOT NULL,
#             created_at   timestamptz NOT NULL DEFAULT now(),
#             resolved_by  uuid REFERENCES users(id),
#             resolved_at  timestamptz
#         );
#         CREATE INDEX IF NOT EXISTS idx_reports_reporter ON reports(reporter_id);
#         CREATE INDEX IF NOT EXISTS idx_reports_target   ON reports(target_type, target_id);
#         """
#             )
            
#             #CREATE TABLE consents IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS consents (
#             user_id         uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
#             email_marketing boolean NOT NULL DEFAULT false,
#             data_sharing    boolean NOT NULL DEFAULT false,
#             updated_at      timestamptz NOT NULL DEFAULT now()
#         );
#         """
#             )
            
#             logger.info("All tables ensured")
            
#             #CREATE helpful Views
#             self.cursor.execute(
#         """
#             CREATE OR REPLACE VIEW event_application_counts AS
#             SELECT
#             e.id AS event_id,
#             COUNT(*) FILTER (WHERE a.status = 'PENDING')  AS pending_count,
#             COUNT(*) FILTER (WHERE a.status = 'APPROVED') AS approved_count,
#             COUNT(*) FILTER (WHERE a.status = 'REJECTED') AS rejected_count
#             FROM events e
#             LEFT JOIN applications a ON a.event_id = e.id
#             GROUP BY e.id;

#             CREATE OR REPLACE VIEW applicant_status_summary AS
#             SELECT
#             u.id AS user_id,
#             COUNT(*) FILTER (WHERE a.status = 'PENDING')   AS pending_count,
#             COUNT(*) FILTER (WHERE a.status = 'APPROVED')  AS approved_count,
#             COUNT(*) FILTER (WHERE a.status = 'REJECTED')  AS rejected_count,
#             COUNT(*) FILTER (WHERE a.status = 'CANCELLED') AS cancelled_count
#             FROM users u
#             LEFT JOIN applications a ON a.applicant_id = u.id
#             GROUP BY u.id;
#         """
#             )
#             self.connection.commit()
#             logger.info("Views created or replaced")
#             data_temp = self.cursor.execute(
#                 """
#                 SELECT * FROM users
#                 """
#             )
#             logger.info(f"Sample data fetched: {data_temp}")
            
            
#         except Exception as e:
#             # Do not re-raise here; keep the module importable even if DB connection fails.
#             logger.exception("Could not initialize database connection: %s", e)
#             self.connection = None
#             self.cursor = None
#         self._initialized = True
    

#     async def execute_query(self, query: str):
#         try:
#             data = await self.cursor.execute(query)
#             await self.connection.commit()
#             return data
#         except Exception as e:
#             logger.error(f"Error executing query: {e}")
#             await self.connection.rollback()
#             return None
        
#     async def fetch_one(self, query: str, params: tuple = ()):
#         try:
#             await self.cursor.execute(query, params)
#             return await self.cursor.fetchone()
#         except Exception as e:
#             logger.error(f"Error fetching one: {e}")
#             return None

#     # Synchronous helpers for blocking psycopg2 usage from sync endpoints
#     def execute_query_sync(self, query: str, params: tuple = ()): 
#         if not self.connection or not self.cursor:
#             logger.error("execute_query_sync called but DB connection is not initialized")
#             return None
#         try:
#             self.cursor.execute(query, params)
#             # try to fetch rows if any
#             if self.cursor.description:
#                 cols = [d.name if hasattr(d, 'name') else d[0] for d in self.cursor.description]
#                 rows = self.cursor.fetchall()
#                 self.connection.commit()
#                 return [dict(zip(cols, r)) for r in rows]
#             else:
#                 self.connection.commit()
#                 return []
#         except Exception as e:
#             logger.error(f"Error executing query sync: {e}")
#             try:
#                 self.connection.rollback()
#             except Exception:
#                 pass
#             return None

#     def fetch_one_sync(self, query: str, params: tuple = ()): 
#         if not self.connection or not self.cursor:
#             logger.error("fetch_one_sync called but DB connection is not initialized")
#             return None
#         try:
#             self.cursor.execute(query, params)
#             row = self.cursor.fetchone()
#             if row and self.cursor.description:
#                 cols = [d.name if hasattr(d, 'name') else d[0] for d in self.cursor.description]
#                 return dict(zip(cols, row))
#             return None
#         except Exception as e:
#             logger.error(f"Error fetching one sync: {e}")
#             try:
#                 self.connection.rollback()
#             except Exception:
#                 pass
#             return None

# #==================================
# # Create a global database instance
# #==================================
# db = DataBase()
# logger.info("Database instance created")


# app = FastAPI(default_response_class=ORJSONResponse, port = env_settings.PORT)

# # Register page auth middleware
# app.add_middleware(PageAuthMiddleware)

# #===================================
# # - middlewares - 
# #===================================
# @app.middleware("http")
# async def security_headers(req: Request, call_next):
#     # Log basic request info so we can see requests arriving in the terminal
#     logger.info(f"Incoming request: {req.method} {req.url}")
#     try:
#         # Try to read body for debug (may be empty or streamed)
#         body = await req.body()
#         if body:
#             try:
#                 logger.debug(f"Request body: {body.decode('utf-8')}")
#             except Exception:
#                 logger.debug(f"Request body (raw bytes, {len(body)} bytes)")
#     except Exception:
#         # If the body cannot be read (e.g., streaming) just continue
#         logger.debug("Could not read request body")

#     start = datetime.utcnow()
#     try:
#         response = await call_next(req)
#         response.headers.update({
#             "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
#             "X-Frame-Options": "DENY",
#             "X-Content-Type-Options": "nosniff",
#             "Referrer-Policy": "no-referrer",
#             "Permissions-Policy": "geolocation=(), microphone=()",
#         })
#     except Exception:
#         # Log exception with full stacktrace then re-raise so exception handlers still run
#         logger.exception("Unhandled exception while handling request")
#         raise
#     duration = (datetime.utcnow() - start).total_seconds()
#     logger.info(f"Completed {req.method} {req.url} -> {response.status_code} in {duration:.3f}s")    
#     return response

# # Trusted hosts
# app.add_middleware(SessionMiddleware, secret_key=env_settings.JWT_SECRET)

# # CORS (chỉ origin frontend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[env_settings.API_ORIGIN] if env_settings.API_ORIGIN else [],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     allow_headers=["Authorization", "Content-Type", "x-csrf"],
# )
# #===================================
# #- Session and CSRF Middleware -
# #===================================
# class CSRFMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.method in ("POST", "PUT", "DELETE", "PATCH"):
#             assert_csrf(request)
#         if "csrf_token" not in request.session:
#             request.session["csrf_token"] = make_csrf()
#         response = await call_next(request)
#         return response


# #========================
# #- api endpoints desgin -
# #========================

# # DEFINE USERS REALTED APIs
# class RegisterRequest(BaseModel):
#     email: str
#     password: str
#     display_name: str
#     type: str = "BOTH"
    
# class LoginRequest(BaseModel):
#     email: str
#     password: str

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     jwt_secret, jwt_algo, access_token_expire_minutes, _, _ = ENV().get_jwt_secret()
#     expire = datetime.now() + (expires_delta or timedelta(minutes=access_token_expire_minutes))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algo)
#     return encoded_jwt

# def verify_access_token(token: str = Depends(ENV().get_jwt_secret()[4])):
#     jwt_secret, jwt_algo, _, _, _ = ENV().get_jwt_secret()
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algo])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         return user_id
#     except Exception:
#         # jose raises JWTError (imported as JWTError) for invalid tokens
#         raise credentials_exception

# def decode_token(token: str):
#     jwt_secret, jwt_algo, _, _, _ = ENV().get_jwt_secret()
#     try:
#         payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algo])
#         return payload
#     except jwt.ExpiredSignatureError:
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# @app.post("/api/register")
# def register(request: RegisterRequest):
#     # simple validation/normalization
#     email = request.email.lower().strip()   
#     cur = db.connection.cursor()
#     # debug
#     logger.debug(f"Registering user with email: {email}")
#     try:
#         # check existing user (parameterized to avoid SQL injection)
#         cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
#         if cur.fetchone():
#             raise fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

#         # hash password using bcrypt
#         pwd_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#         # insert new user and return created fields
#         cur.execute(
#             """
#             INSERT INTO users (email, password_hash, display_name, type)
#             VALUES (%s, %s, %s, %s)
#             RETURNING id, email, display_name, type, is_active, created_at
#             """,
#             (email, pwd_hash, request.display_name, request.type),
#         )
#         row = cur.fetchone()
#         db.connection.commit()

#         # return created user (as dict)
#         if row:
#             cols = [d[0] for d in cur.description]
#             return dict(zip(cols, row))
#         else:
#             raise fastapi.HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
#     # Handle unique constraint violation (email already exists)
#     except psycopg2.IntegrityError:
#         db.connection.rollback()
#         # Log detailed DB integrity error if available and return 409
#         logger.exception("Integrity error while creating user (possible duplicate email)")
#         db.connection.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
#     # Handle other database errors
#     except Exception as e:
#         # If the exception is already an HTTPException we raised intentionally, re-raise it
#         if isinstance(e, HTTPException):
#             raise
#         db.connection.rollback()
#         logger.exception("Error creating user: %s", e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
#     finally:
#         try:
#             cur.close()
#         except Exception:
#             pass

# @app.post("/api/login")
# def login(request: LoginRequest):
#     _, _, _, refresh_token_expire_minutes, _ = ENV().get_jwt_secret()
#     # normalize email before lookup
#     email = request.email.lower().strip()
#     cur= db.connection.cursor()
#     cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
#     user = cur.fetchone()
#     cur.close()

#     if not user:
#         raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
#     user_id, pwd_hash = user

#     if not bcrypt.checkpw(request.password.encode('utf-8'), pwd_hash.encode('utf-8')):
#         raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
#     access_token = create_access_token(data={"sub": str(user_id), "email": email})
#     refresh_token = create_access_token(data={"sub": str(user_id), "email": email}, expires_delta=timedelta(minutes=refresh_token_expire_minutes))

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#         "user": {"id": str(user_id), "email": email}
#     }
# # def login(request: LoginRequest):
# #     query = f"SELECT password_hash FROM users WHERE email = '{request.email}'"
# #     user = db.execute_query(query)
# #     if user and bcrypt.checkpw(request.password.encode('utf-8'), user[0]['password_hash'].encode('utf-8')):
# #         return {"message": "Login successful"}
#     # return {"message": "Invalid email or password"}, 401



# class ProfileRequest(BaseModel):
#     user_id: str
    
# @app.get("/api/profile")
# @app.post("/api/profile")
# def profile(request: ProfileRequest):
#     query = f"SELECT id, email, display_name, type, is_active, created_at, updated_at FROM users WHERE id = '{request.user_id}'"
#     user = db.execute_query(query)
#     if user:
#         return {"user": user[0]}, 200
#     return {"message": "User not found"}, 404



# # EVENT APIs
# @app.get("/api/events")
# def events(request: Request):
#     assert_csrf(request)
#     query = "SELECT id, title, description, start_time, end_time, location FROM events"
#     events = db.execute_query_sync(query)
#     if events:
#         return {"events": events}, 200
#     return {"message": "No events found"}, 404

# class createEventRequest(BaseModel):
#     title: str
#     description: str
#     location: str
#     starts_at: str  # ISO 8601 format
#     ends_at: str    # ISO 8601 format
#     capacity: int
#     organizer_id: str
# @app.post("/api/events")
# def create_event(request: createEventRequest):
#     query = f"""
#     INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by)
#     VALUES ('{request.title}', '{request.description}', '{request.location}', '{request.starts_at}', '{request.ends_at}', {request.capacity}, '{request.organizer_id}')
#     RETURNING id;
#     """
#     event_id = db.execute_query(query)
#     if event_id:
#         return {"message": "Event created successfully", "event_id": event_id[0]['id']}, 201
#     return {"message": "Failed to create event"}, 500

# class UpdateEventRequest(BaseModel):
#     event_id: str
#     title: str
#     description: str
#     location: str
#     starts_at: str  # ISO 8601 format
#     ends_at: str    # ISO 8601 format
#     capacity: int
#     organizer_id: str
# @app.put("/api/events")
# def update_event(request: UpdateEventRequest, req: Request):
#     assert_csrf(req)
#     query = "SELECT created_by FROM events WHERE id = %s"
#     event = db.fetch_one_sync(query, (request.event_id,))
#     if not event:
#         return {"message": "Event not found"}, 404
#     if event['created_by'] != request.organizer_id:
#         return {"message": "Unauthorized"}, 403

#     query = """UPDATE events
#     SET title = %s,
#         description = %s,
#         location = %s,
#         starts_at = %s,
#         ends_at = %s,
#         capacity = %s,
#         updated_at = now()
#     WHERE id = %s;"""

#     success = db.execute_query_sync(query, (request.title, request.description, request.location, request.starts_at, request.ends_at, request.capacity, request.event_id))
#     if success is not None:
#         return {"message": "Event updated successfully"}, 200
    
#     return {"message": "Failed to update event"}, 500