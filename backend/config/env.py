import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
class ENV:
    #read .env in the root directory
    #load .env variables into ENV class attributes
    #for example, ENV.DB_HOST = os.getenv("DB_HOST")
    
    def __init__(self):
        # Read .env values first, then fall back to environment variables.
        self.DATABASE_USER = os.getenv("DATABASE_USER")
        self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
        self.DATABASE_HOST = os.getenv("DATABASE_HOST")
        self.DATABASE_NAME = os.getenv("DATABASE_NAME")
        self.PORT = os.getenv("PORT", 8000)
        self.JWT_SECRET = os.getenv("JWT_SECRET", "super-long-random-string")
        self.JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
        self.REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "7"))
        self.COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")  
        self.BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.API_ORIGIN = os.getenv("API_ORIGIN") 
        self.ALLOWED_HOSTS = (os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")).split(",")

    
    # PORT = int(os.getenv("PORT", "8000"))
    def get_db_url(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}/{self.DATABASE_NAME}?sslmode=require&channel_binding=require"
    
    def get_port(self):
        return int(self.PORT)

    # JWT CONFIG 
    def get_jwt_secret(self):
        return (
            self.JWT_SECRET, 
            self.JWT_ALGO, 
            self.ACCESS_TOKEN_EXPIRE_MINUTES, 
            self.REFRESH_TOKEN_EXPIRE_MINUTES, 
            OAuth2PasswordBearer(tokenUrl="/api/login")
        )
env_settings = ENV()
