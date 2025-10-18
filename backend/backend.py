import fastapi 
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2
import os,time, uuid, secrets
from .config.logger import logger
import bcrypt
import threading

# from transformers import Optional

from fastapi import FastAPI,HTTPException,security, Depends, Request,status, APIRouter
from fastapi.responses import ORJSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
# from models import User, Event, Application
from fastapi import Request, Response
from typing import Callable, Optional
# from security_cookies import create_access_token, create_refresh_token, get_current_user, require_roles

# from jose import JWTError, jwt
from passlib.context import CryptContext

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from datetime import datetime, timedelta

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


# check connect
# print("DB_HOST:", os.getenv("DATABASE_HOST")) 
#============ENVIRONMENT SETTINGS=================================
from .config.env import ENV,env_settings
from .config.logger import logger
# ============MIDDLEWARES=================================
from .middlewares.setup import setup_middlewares
#==========================SECURTY=============================================================
from .config.security import create_access_token, assert_csrf, require_roles


#===============================================DATABASE========================================
# initialize database connection and use instance pattern for this class

#==================================
# Create a global database instance
#==================================
from .db.database import db
# ================APP INITIALIZATION==============================
app = FastAPI(default_response_class=ORJSONResponse)
setup_middlewares(app)
#========================
#- api endpoints desgin -
#========================

# DEFINE USERS REALTED APIs
class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str
    type: str = "BOTH"
    
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/register")
def register(request: RegisterRequest):
    # simple validation/normalization
    email = request.email.lower().strip()
    cur = db.connection.cursor()
    # debug
    logger.debug(f"Registering user with email: {email}")
    try:
        # check existing user (parameterized to avoid SQL injection)
        cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # hash password using bcrypt
        pwd_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # insert new user and return created fields
        cur.execute(
            """
            INSERT INTO users (email, password_hash, display_name, type)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, display_name, type, is_active, created_at
            """,
            (email, pwd_hash, request.display_name, request.type),
        )
        row = cur.fetchone()
        db.connection.commit()

        # return created user (as dict)
        if row:
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
        else:
            raise fastapi.HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    # Handle unique constraint violation (email already exists)
    except psycopg2.IntegrityError:
        db.connection.rollback()
        # Log detailed DB integrity error if available and return 409
        logger.exception("Integrity error while creating user (possible duplicate email)")
        db.connection.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    # Handle other database errors
    except Exception as e:
        # If the exception is already an HTTPException we raised intentionally, re-raise it
        if isinstance(e, HTTPException):
            raise
        db.connection.rollback()
        logger.exception("Error creating user: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    finally:
        try:
            cur.close()
        except Exception:
            pass

@app.post("/auth/login")
def login(request: LoginRequest):
    _, _, _, refresh_token_expire_minutes, _ = ENV().get_jwt_secret()
    # normalize email before lookup
    email = request.email.lower().strip()
    cur= db.connection.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    user_id, pwd_hash = user

    if not bcrypt.checkpw(request.password.encode('utf-8'), pwd_hash.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": str(user_id), "type": "access", "email": email})
    refresh_token = create_access_token(
        data={"sub": str(user_id), "type": "refresh", "email": email},
        expires_delta=timedelta(minutes=refresh_token_expire_minutes)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {"id": str(user_id), "email": email}
    }


class ProfileRequest(BaseModel):
    user_id: str
    
@app.get("/api/profile")
@app.post("/api/profile")
def profile(request: ProfileRequest):
    query = f"SELECT id, email, display_name, type, is_active, created_at, updated_at FROM users WHERE id = '{request.user_id}'"
    user = db.execute_query_sync(query)
    if user:
        return {"user": user[0]}, 200
    return {"message": "User not found"}, 404



# EVENT APIs
@app.get("/api/events")
def events(request: Request):
    assert_csrf(request)
    query = "SELECT id, title, description, start_time, end_time, location FROM events"
    events = db.execute_query_sync(query)
    if events:
        return {"events": events}, 200
    return {"message": "No events found"}, 404

class createEventRequest(BaseModel):
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int
    organizer_id: str
@app.post("/api/events")
def create_event(request: createEventRequest):
    query = f"""
    INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by)
    VALUES ('{request.title}', '{request.description}', '{request.location}', '{request.starts_at}', '{request.ends_at}', {request.capacity}, '{request.organizer_id}')
    RETURNING id;
    """
    event_id = db.execute_query(query)
    if event_id:
        return {"message": "Event created successfully", "event_id": event_id[0]['id']}, 201
    return {"message": "Failed to create event"}, 500

class UpdateEventRequest(BaseModel):
    event_id: str
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int
    organizer_id: str
@app.put("/api/events")
def update_event(request: UpdateEventRequest, req: Request):
    assert_csrf(req)
    query = "SELECT created_by FROM events WHERE id = %s"
    event = db.fetch_one_sync(query, (request.event_id,))
    if not event:
        return {"message": "Event not found"}, 404
    if event['created_by'] != request.organizer_id:
        return {"message": "Unauthorized"}, 403

    query = """UPDATE events
    SET title = %s,
        description = %s,
        location = %s,
        starts_at = %s,
        ends_at = %s,
        capacity = %s,
        updated_at = now()
    WHERE id = %s;"""

    success = db.execute_query_sync(query, (request.title, request.description, request.location, request.starts_at, request.ends_at, request.capacity, request.event_id))
    if success is not None:
        return {"message": "Event updated successfully"}, 200
    
    return {"message": "Failed to update event"}, 500