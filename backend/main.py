import fastapi 
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
# from models import User, Event, Application
from fastapi import Request, Response
# from security_cookies import create_access_token, create_refresh_token, get_current_user, require_roles


from fastapi import Depends, HTTPException, status

# check connect
# print("DB_HOST:", os.getenv("DATABASE_HOST")) 
#============ENVIRONMENT SETTINGS=================================
from .config.env import ENV,env_settings
from .config.logger import logger
# ============MIDDLEWARES=================================
from .middlewares.setup import setup_middlewares

# ================APP INITIALIZATION==============================
app = FastAPI(default_response_class=ORJSONResponse)
setup_middlewares(app)
#========================
#- api endpoints desgin -
#========================
from .routes.auth_route import router as auth_router
from .routes.user_route import router as user_router
from .routes.events_route import router as events_router

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(events_router, prefix="/events", tags=["Events"])

"""
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
"""