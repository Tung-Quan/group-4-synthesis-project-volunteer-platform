from ..models.user_models import RegisterRequest, LoginRequest
from ..config.logger import logger
from ..config.env import ENV
from ..config.security import create_access_token, hash_password, verify_password
from ..db.database import db
from datetime import timedelta
import psycopg2

def register(request: RegisterRequest) -> dict:
    # simple validation/normalization
    email = request.email.lower().strip()
    valid_types = {'STUDENT', 'ORGANIZER'}
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
            # cols = [d[0] for d in cur.description]
            # return dict(zip(cols, row))
            return new_user_row[0]
        else:
            return {"error": "Failed to create user", "status_code": 500}
    # Handle unique constraint violation (email already exists)
    except psycopg2.IntegrityError as e:
        # Log detailed DB integrity error if available and return 409
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

    access_token = create_access_token(data={"sub": user_id, "type": "access"})
    refresh_token = create_access_token(
        data={"sub": user_id, "type": "refresh"},
        expires_delta=timedelta(minutes=refresh_token_expire_minutes)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {"id": user_id, "email": email}
    }
