from ..models.user_models import UpdateProfileRequest, UserProfileResponse
from ..config.logger import logger
from ..db.database import db

def get_user_profile(user_id: str) -> dict:
    query = """
    SELECT id, email, display_name, type, is_active, created_at
    FROM users
    WHERE id = %s
    """
    user_row = db.fetch_one_sync(query, (user_id,))
    if user_row:
        return user_row
    else:
        return {"error": "User not found", "status_code": 404}
    
def update_user_profile(user_id: str, request: UpdateProfileRequest) -> dict:
    update_fields = []
    params = []

    if request.display_name is not None:
        update_fields.append("display_name = %s")
        params.append(request.display_name)

    # Check if need to update
    if not update_fields:
        return {"error": "No fields to update", "status_code": 400}
    
    params.append(user_id)

    query = """
    UPDATE users
    SET{", ".join(update_fields), updated_at = NOW()}
    WHERE id = %s
    ReTURNING id, email, display_name, type, is_active, created_at
    """
    updated_user_row = db.execute_query_sync(query, tuple(params))

    if updated_user_row:
        return updated_user_row[0]
    else:
        return {"error": "Failed to update profile", "status_code": 500}