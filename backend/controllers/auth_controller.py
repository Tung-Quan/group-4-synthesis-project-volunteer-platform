from ..models.user_models import RegisterRequest, LoginRequest
from ..config.logger import logger
from ..config.env import ENV
from ..config.security import create_access_token, hash_password, verify_password
from ..db.database import db
from datetime import timedelta
from ..config.security import make_csrf
import psycopg2

import jwt
from jwt import PyJWTError


def register(request: RegisterRequest) -> dict:
    # simple validation/normalization
    email = request.email.lower().strip()
    valid_types = {'STUDENT', 'ORGANIZER'}
    # debug
    logger.debug(f"Registering user: {email} as {request.type}")

    # Check for non-empty fields
    if not email or not request.password:
        return {"error": "Email and password are required", "status_code": 400}
    # If type present, validate
    if request.type and request.type not in valid_types:
        return {"error": "Invalid type", "status_code": 400}
    # Check if user already exists
    existing_user = db.fetch_one_sync(
        "SELECT 1 FROM users WHERE email = %s", (email,))
    if existing_user:
        return {"error": "Email already registered", "status_code": 409}

    pwd_hash = hash_password(request.password)
    query = """
    INSERT INTO users (email, password_hash, full_name, phone, type)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id, email, full_name, phone, type, is_active, created_at, updated_at
    """
    params = (email, pwd_hash, request.full_name, request.phone, request.type)

    try:
        new_user_row = db.execute_query_sync(query, params)

        if new_user_row:
            user = new_user_row[0]
            user_id = user.get('id')

            # INSERT type INFO
            try:
                if request.type == 'STUDENT':
                    if not request.student_no:
                        db.execute_query_sync(
                            "DELETE FROM users WHERE id = %s", (user_id,))
                        return {"error": "student_no required", "status_code": 400}
                    db.execute_query_sync(
                        "INSERT INTO students (user_id, student_no) VALUES (%s, %s)", (user_id, request.student_no))

                elif request.type == 'ORGANIZER':
                    if not request.organizer_no:
                        db.execute_query_sync(
                            "DELETE FROM users WHERE id = %s", (user_id,))
                        return {"error": "organizer_no required", "status_code": 400}
                    db.execute_query_sync("INSERT INTO organizers (user_id, organizer_no, org_name) VALUES (%s, %s, %s)", (
                        user_id, request.organizer_no, request.org_name))

            except Exception as e:
                logger.exception(f"Failed to create type record: {e}")
                db.execute_query_sync(
                    "DELETE FROM users WHERE id = %s", (user_id,))
                return {"error": "Registration failed. Please try again.", "status_code": 500}

            return user
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

    user = db.fetch_one_sync(
        "SELECT id, email, password_hash, type FROM users WHERE email = %s", (email,))

    if not user or not verify_password(request.password, user['password_hash']):
        return {"error": "Invalid email or password", "status_code": 401}

    _, _, _, refresh_token_expire_minutes, _ = ENV().get_jwt_secret()
    user_id = str(user['id'])

    access_token = create_access_token(
        data={"sub": user_id}, token_type="access")
    refresh_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=refresh_token_expire_minutes),
        token_type="refresh",
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {"id": user_id, "email": email, "type": user['type']}
    }


def logout(request, response, user_id: str) -> dict:
    # For JWT, logout is typically handled client-side by deleting tokens (cookies).
    cookie_domain = getattr(ENV(), 'COOKIE_DOMAIN', None)
    try:
        response.delete_cookie(
            key="access_token", path='/', domain=cookie_domain)
        response.delete_cookie(key="refresh_token",
                               path='/auth/refresh', domain=cookie_domain)
        # response.delete_cookie(key="session", path='/', domain=cookie_domain) #delete session cookie
    except Exception:
        # fallback to simple deletion if domain/path fails
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        # response.delete_cookie(key="session
        # ") #delete session cookie
    try:
        # if "csrf_token" in request.session:
        request.session.pop("csrf_token", None)
        # None
    except Exception:
        pass

    logger.info(f"User {user_id} logged out. (logout handler executed)")

    return {"message": "Logout successful", "user_id": user_id}


def attach_csrf_token(session: dict) -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = make_csrf()
    return session["csrf_token"]


def regenerate_csrf_token(session: dict) -> str:
    """
    tạo mới CSRF token và ghi đè lên cái cũ.
    Dùng riêng cho hành động Login để bảo mật (Session Rotation).
    """
    new_token = make_csrf()
    session["csrf_token"] = new_token
    return new_token


def refresh(refresh_token: str) -> dict:
    try:
        jwt_secret, jwt_algo, _, _, _ = ENV().get_jwt_secret()

        payload = jwt.decode(
            refresh_token,
            jwt_secret,
            algorithms=[jwt_algo]
        )

        if payload.get("type") != "refresh":
            return {"error": "Invalid token type", "status_code": 401}

        user_id = payload.get("sub")

        # Tạo lại access token
        new_access_token = create_access_token(
            data={"sub": user_id, "type": "access"}
        )

        return {"access_token": new_access_token}

    except PyJWTError:
        return {"error": "Invalid refresh token", "status_code": 401}
