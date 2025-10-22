from ..models.user_models import RegisterRequest, LoginRequest
from ..config.logger import logger
from ..config.env import ENV
from ..config.security import create_access_token, hash_password, verify_password
from ..db.database import db
from datetime import timedelta
from ..config.security import make_csrf
import psycopg2

def register(request: RegisterRequest) -> dict:
    # simple validation/normalization
    email = request.email.lower().strip()
    valid_types = {'STUDENT', 'ORGANIZER','BOTH'}
    # debug
    logger.debug(f"Registering user with email: {email}")

    # Check for non-empty fields
    if not email or not request.password or not request.display_name or not request.type:
        return {"error": "All fields are required", "status_code": 400}
    # Check if role is valid
    # Khang: need to fix to student only after testing
    if request.type not in valid_types:
        return {"error": "Invalid user type", "status_code": 400}
    # Check if user already exists
    existing_user = db.fetch_one_sync("SELECT 1 FROM users WHERE email = %s", (email,))
    if existing_user:
        return {"error": "Email already registered", "status_code": 409}
    

    pwd_hash = hash_password(request.password)
    query = """
    INSERT INTO users (email, password_hash, display_name, type)
    VALUES (%s, %s, %s, %s)
    RETURNING id, email, display_name, type, is_active, created_at
    """
    params = (email, pwd_hash, request.display_name, request.type)

    try:
        new_user_row = db.execute_query_sync(query, params)
        # return created user
        if new_user_row:
            return new_user_row[0]
        else:
            return {"error": "Failed to create user", "status_code": 500}
    # Handle unique constraint violation (email already exists)
    except psycopg2.IntegrityError as e:
        logger.exception("Database integrity error during registration: %s", e)
        # catch error when db take 2 requests to create same email at the same time
        return {"error": "Database error during registration", "status_code": 500}

def login(request: LoginRequest) -> dict:
    # normalize email before lookup
    email = request.email.lower().strip()

    user = db.fetch_one_sync("SELECT id, password_hash FROM users WHERE email = %s", (email,))

    if not user or not verify_password(request.password, user['password_hash']):
        return {"error": "Invalid email or password", "status_code": 401}
    
    _, _, _, refresh_token_expire_minutes, _ = ENV().get_jwt_secret()
    user_id = str(user['id'])

    access_token = create_access_token(data={"sub": user_id}, token_type="access")
    refresh_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=refresh_token_expire_minutes),
        token_type="refresh",
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {"id": user_id, "email": email}
    }

def logout(request, response, user_id: str) -> dict:
    # For JWT, logout is typically handled client-side by deleting tokens (cookies).
    cookie_domain = getattr(ENV(), 'COOKIE_DOMAIN', None)
    try:
        response.delete_cookie(key="access_token", path='/', domain=cookie_domain)
        response.delete_cookie(key="csrf_token", path='/', domain=cookie_domain)
        # response.delete_cookie(key="session", path='/', domain=cookie_domain) #delete session cookie
    except Exception:
        # fallback to simple deletion if domain/path fails
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="csrf_token")
        # response.delete_cookie(key="session
        # ") #delete session cookie
    try:
        # if "csrf_token" in request.session:
        #     request.session.pop("csrf_token", None)
        None
        # request.session.clear()  # Xóa toàn bộ session
    except Exception:
        pass

    logger.info(f"User {user_id} logged out. (logout handler executed)")
    
    return {"message": "Logout successful", "user_id": user_id}

def attach_csrf_token(session: dict) -> str:
    if "csrf_token" not in session:
        session["csrf_token"]= make_csrf()
    return session["csrf_token"]