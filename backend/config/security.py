import bcrypt
import jwt
import secrets
from fastapi import HTTPException, Depends, Request
from datetime import timedelta
from .env import env_settings
from ..db.database import db
from datetime import datetime


#=======================
#-Token data model
#=======================
# # class TokenData(BaseModel):
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

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    jwt_secret, jwt_algo, access_token_expire_minutes, _, _ = env_settings.get_jwt_secret()
    expire = datetime.now() + (expires_delta or timedelta(minutes=access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algo)
    return encoded_jwt
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
#     except jwt.PyJWTError:
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
def make_csrf() -> str:
    return secrets.token_urlsafe(32)

def assert_csrf(request):
    session_token = request.session.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")
    if not session_token or not header_token or session_token != header_token:
        raise HTTPException(status_code=403, detail="CSRF token missing or invalid")
    return True

# async def current_user(req: Request):
#     tok = req.cookies.get("access")
#     if not tok: 
#         raise HTTPException(401, "Missing token")
#     data = decode_jwt(tok)
#     if data.type != "access": 
#         raise HTTPException(401, "Wrong token type")
#     user = (await db.execute(select(User).where(User.id == data.sub))).scalar_one_or_none()
#     if not user:
#         raise HTTPException(401, "User not found")
#     return user
async def current_user(req: Request) -> dict:
    tok = req.cookies.get("access")
    if not tok: 
        raise HTTPException(401, "Missing token")
    payload = jwt.decode(tok, env_settings.JWT_SECRET, algorithms=[env_settings.JWT_ALGO])
    if payload.get("type") != "access": 
        raise HTTPException(401, "Wrong token type")
    user = db.fetch_one_sync("SELECT * FROM users WHERE id = %s", (payload["sub"],))
    if not user:
        raise HTTPException(401, "User not found")
    return user

# def require_roles(*roles: str):
#     async def dep(u: User = Depends(current_user)):
#         if u.role not in roles:
#             raise HTTPException(403, "Insufficient role")
#         return u
#     return dep
def require_roles(*roles: str):
    async def dep(u: dict = Depends(current_user)):
        user_type = u.get('type', 'BOTH')
        if user_type not in roles:
            raise HTTPException(403, "Insufficient role")
        return u
    return dep