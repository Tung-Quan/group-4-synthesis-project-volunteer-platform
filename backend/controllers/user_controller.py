from ..models.user_models import *
from ..config.logger import logger
from ..db.database import db
from fastapi import Request
from ..config.security import assert_csrf
import json

#@app.get("/api/profile")
def view_profile(request: ViewProfileRequest):
    query = f"""
        SELECT id, email, display_name, type, is_active, created_at, updated_at
        FROM users
        WHERE id = '{request.user_id}';
    """
    user = db.execute_query_sync(query)
    if not user:
        return {"message": "User not found"}, 404
    return {"message": "Successfully!"}, 200
