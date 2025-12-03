import bcrypt
import jwt
import secrets
from .env import env_settings
from datetime import timedelta, datetime, UTC

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None, token_type: str = "access"):
    """Create a JWT with explicit token_type. The caller should pass token_type='access' or 'refresh'.
    This avoids relying on the caller to include a 'type' field in `data` which could be overwritten.
    """
    to_encode = data.copy()

    jwt_secret, jwt_algo, access_token_expire_minutes, _, _ = env_settings.get_jwt_secret()

    # Use UTC times
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=access_token_expire_minutes)

    # set type explicitly from parameter
    to_encode.update({"exp": expire, "iat": now, "type": token_type})

    # Support alg='none' explicitly
    if isinstance(jwt_algo, str) and jwt_algo.lower() == "none":
        encoded_jwt = jwt.encode(to_encode, key=None, algorithm=None)
    else:
        encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algo)
    return encoded_jwt

def make_csrf() -> str:
    return secrets.token_urlsafe(32)


