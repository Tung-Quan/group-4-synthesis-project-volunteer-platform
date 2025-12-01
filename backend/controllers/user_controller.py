from ..models.user_models import UpdateProfileRequest, UserProfileResponse
from ..config.logger import logger
from ..db.database import db


def get_user_profile(user_id: str) -> dict:
    """
    Lấy thông tin profile chi tiết kèm thống kê dựa trên role.
    """
    # 1. Lấy thông tin cơ bản
    query_user = """
    SELECT id, email, full_name, phone, type, is_active, created_at, updated_at
    FROM users
    WHERE id = %s
    """
    user_row = db.fetch_one_sync(query_user, (user_id,))

    if not user_row:
        return {"error": "User not found", "status_code": 404}
    user_type = user_row['type']

    # 2. Phân nhánh logic (Chỉ còn STUDENT hoặc ORGANIZER)
    if user_type == 'STUDENT':
        query_joined = "SELECT COUNT(*) as count FROM applications WHERE student_user_id = %s AND status = 'attended'"

        # fetch_one_sync trả về dict, lấy key 'count'
        joined_res = db.fetch_one_sync(query_joined, (user_id,))
        joined_count = joined_res['count'] if joined_res else 0

        # b. Lấy thông tin sinh viên (MSSV, ngày CTXH)
        query_student_info = "SELECT student_no, social_work_days FROM students WHERE user_id = %s"
        student_info = db.fetch_one_sync(query_student_info, (user_id,))

        total_days = float(
            student_info['social_work_days']) if student_info else 0.0

        # c. Đếm số đơn đang chờ (applied/pending)
        query_pending = """
            SELECT COUNT(*) as count 
            FROM applications 
            WHERE student_user_id = %s AND status IN ('applied')
        """
        pending_res = db.fetch_one_sync(query_pending, (user_id,))
        pending_count = pending_res['count'] if pending_res else 0

        # d. Gộp tất cả lại
        return {
            **user_row,
            "student_info": student_info,
            "stats": {
                "activities_joined": joined_count,
                "total_social_work_days": total_days,
                "pending_activities": pending_count
            }
        }

    # 3. Nếu là ORGANIZER -> Lấy thêm stats của Organizer
    elif user_type == 'ORGANIZER':
        # a. Lấy thông tin tổ chức
        query_org_info = "SELECT organizer_no, org_name FROM organizers WHERE user_id = %s"
        org_info = db.fetch_one_sync(query_org_info, (user_id,))

        # b. Đếm số event đã tạo
        query_events = """
            SELECT COUNT(*) as count 
            FROM events 
            WHERE organizer_user_id = %s
        """
        event_res = db.fetch_one_sync(query_events, (user_id,))
        event_count = event_res['count'] if event_res else 0

        return {
            **user_row,
            "organizer_info": org_info,
            "stats": {
                "managed_events_count": event_count
            }
        }

    # Nếu no roles or BOTH -> Trả về cơ bản
    return user_row


def update_user_profile(user_id: str, request: UpdateProfileRequest) -> dict:
    """
    Cập nhật thông tin profile (full_name, phone).
    """
    update_fields = []
    params = []

    if request.full_name is not None:
        update_fields.append("full_name = %s")
        params.append(request.full_name)
    if request.phone is not None:
        update_fields.append("phone = %s")
        params.append(request.phone)

    # Nếu không có gì để update -> Báo lỗi nhẹ
    if not update_fields:
        return {"error": "No fields to update", "status_code": 400}

    params.append(user_id)

    # Tạo câu lệnh SQL động
    set_clause = ", ".join(update_fields) + ", updated_at = NOW()"

    # Dùng f-string đúng cách (chỉ ghép chuỗi lệnh, không ghép giá trị)
    query = f"""
    UPDATE users
    SET {set_clause}
    WHERE id = %s
    RETURNING id, email, full_name, phone, type, is_active, created_at, updated_at
    """

    updated_user_row = db.execute_query_sync(query, tuple(params))

    if updated_user_row:
        # Return the enriched profile (roles/type/stats) to satisfy response model
        return get_user_profile(user_id)
    else:
        return {"error": "Failed to update profile", "status_code": 500}
