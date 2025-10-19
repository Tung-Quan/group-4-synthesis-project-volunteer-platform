import bcrypt
import jwt
import secrets
from .env import env_settings
from datetime import timedelta, datetime

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    jwt_secret, jwt_algo, access_token_expire_minutes, _, _ = env_settings.get_jwt_secret()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algo)
    return encoded_jwt

def make_csrf() -> str:
    return secrets.token_urlsafe(32)


