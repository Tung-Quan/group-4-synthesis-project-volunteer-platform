from ..models.event_models import *
from ..config.logger import logger
from ..db.database import db
from fastapi import Request
from ..dependencies import verify_csrf
import json

def get_events():
    query = """SELECT * FROM events"""
    events = db.execute_query_sync(query)
    if not events:
        return None
    return events

def get_own_events(my_id):
    query = """SELECT * FROM events WHERE organizer_user_id = %s"""
    events = db.execute_query_sync(query,(my_id,))
    if not events:
        return None
    return events

def get_upcoming_events():
    """
    Lấy các sự kiện MỚI (Chưa bắt đầu slot nào).
    Sắp xếp: Sự kiện nào diễn ra sớm nhất thì lên đầu.
    """
    query = """
        SELECT 
            e.id, e.title, e.description, e.location, e.status,
            e.organizer_user_id,
            o.org_name,
            -- Lấy thời gian bắt đầu sớm nhất của event này
            MIN(s.work_date + s.starts_at) as event_start_time,
            -- Lấy thời gian kết thúc muộn nhất
            MAX(s.work_date + s.ends_at) as event_end_time,
            -- Đếm tổng số slot
            COUNT(s.id) as total_slots
        FROM events e
        JOIN event_slots s ON e.id = s.event_id
        JOIN organizers o ON e.organizer_user_id = o.user_id
        WHERE e.status = 'published'
        GROUP BY e.id, o.org_name
        -- ĐIỀU KIỆN : Slot sớm nhất phải nằm ở tương lai
        HAVING MIN(s.work_date + s.starts_at) > NOW()
        ORDER BY event_start_time ASC
    """
    return db.execute_query_sync(query)

def get_ongoing_events():
    """
    Lấy các sự kiện ĐANG DIỄN RA (Đã bắt đầu nhưng chưa kết thúc).
    Sắp xếp: Sự kiện nào sắp kết thúc thì lên đầu (để tạo cảm giác gấp rút).
    """
    query = """
        SELECT 
            e.id, e.title, e.description, e.location, e.status,
            e.organizer_user_id,
            o.org_name,
            MIN(s.work_date + s.starts_at) as event_start_time,
            MAX(s.work_date + s.ends_at) as event_end_time,
            COUNT(s.id) as total_slots
        FROM events e
        JOIN event_slots s ON e.id = s.event_id
        JOIN organizers o ON e.organizer_user_id = o.user_id
        WHERE e.status = 'published'
        GROUP BY e.id, o.org_name
        -- ĐIỀU KIỆN: Đã bắt đầu (MIN <= NOW) VÀ Chưa kết thúc (MAX >= NOW)
        HAVING MIN(s.work_date + s.starts_at) <= NOW() 
           AND MAX(s.work_date + s.ends_at) >= NOW()
        ORDER BY event_end_time ASC
    """
    return db.execute_query_sync(query)

def get_event_by_id(id: str):
    query = """
            SELECT e.id, e.organizer_user_id, e.title, e.description, e.location, e.status,
                    s.id AS slot_id, s.work_date, s.starts_at, s.ends_at, s.capacity, s.day_reward
            FROM events e
            LEFT JOIN event_slots s ON e.id = s.event_id
            WHERE e.id = %s
            """
    results = db.execute_query_sync(query, (id,))
    if not results:
        return None
    
    base = results[0]
    event = {
        "id": base["id"],
        "organizer_user_id": base["organizer_user_id"],
        "title": base["title"],
        "description": base["description"],
        "location": base["location"],
        "status": base["status"],
        "slots": []
    }

    for r in results:
        if r["slot_id"] is None:
            continue

        event["slots"].append({
            "slot_id": r["slot_id"],
            "work_date": r["work_date"],
            "starts_at": r["starts_at"],
            "ends_at": r["ends_at"],
            "capacity": r["capacity"],
            "day_reward": float(r["day_reward"]),
        })
    return event

def create_event(request, organizer_id):
    try:
        query = """
            INSERT INTO events (organizer_user_id, title, description, location, status)
            VALUES (%s, %s, %s, %s, 'published')
            RETURNING id;
            """
        db.cursor.execute(query, (
            organizer_id,
            request.title,
            request.description,
            request.location,
        ))

        res = db.cursor.fetchone()
        if not res:
            db.connection.rollback()
            return None
        
        event_id = res[0]

        slot_query = """
                    INSERT INTO event_slots (event_id, work_date, starts_at, ends_at, capacity, day_reward)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """
        slot_ids = []
        for slots in request.slots:
            db.cursor.execute(slot_query, (
                event_id,
                slots.work_date,
                slots.starts_at,
                slots.ends_at,
                slots.capacity,
                slots.day_reward
            ))
            row = db.cursor.fetchone()
            if row is None:
                raise Exception("Failed to insert slot")
            slot_ids = row[0]
        
        db.connection.commit()
        return {"event_id": event_id, "slot_ids": slot_ids}
    
    except Exception as e:
        db.connection.rollback()
        logger.error(f"Error creating event: {e}")
        return None


def update_event_info(event_id, request, organizer_id):
    check_query = """
                SELECT id, organizer_user_id
                FROM events
                WHERE id = %s AND organizer_user_id = %s;
                """
    res = db.execute_query_sync(check_query, (event_id, organizer_id))
    if not res:
        return None

    query = """
        UPDATE events
        SET 
            title = COALESCE(%s, title),
            description = COALESCE(%s, description),
            location = COALESCE(%s, location),
            status = COALESCE(%s, status),
            updated_at = now()
        WHERE id = %s AND organizer_user_id = %s
        RETURNING id;
    """
    params = [
        request.title,
        request.description,
        request.location,
        request.status,
        event_id,
        organizer_id
    ]
    results = db.execute_query_sync(query, tuple(params))
    if not results:
        return None
    return {"event_id": results[0]["id"]}

#  --------------- EVENT_SLOT ---------------
# 1. Thêm Slot vào Event
def add_slot_to_event(event_id: str, request, organizer_id: str):
    # Bước 1: Kiểm tra xem Event có tồn tại và thuộc về Organizer này không
    check_query = "SELECT id FROM events WHERE id = %s AND organizer_user_id = %s"
    event = db.fetch_one_sync(check_query, (event_id, organizer_id))
    
    if not event:
        return {"message": "Event not found or you don't have permission"}, 404

    # Bước 2: Insert Slot
    insert_query = """
        INSERT INTO event_slots (event_id, work_date, starts_at, ends_at, capacity, day_reward)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, event_id, work_date, starts_at, ends_at, capacity, day_reward;
    """
    params = (
        event_id, 
        request.work_date, 
        request.starts_at, 
        request.ends_at, 
        request.capacity, 
        request.day_reward
    )
    
    new_slot = db.fetch_one_sync(insert_query, params)
    
    if not new_slot:
        return {"message": "Failed to create slot"}, 500
        
    return new_slot, 201

# 2. Xóa Slot
def delete_slot(slot_id: str, organizer_id: str):
    # 1. Kiểm tra quyền sở hữu
    check_query = """
        SELECT s.id 
        FROM event_slots s
        JOIN events e ON e.id = s.event_id
        WHERE s.id = %s AND e.organizer_user_id = %s
    """
    slot = db.fetch_one_sync(check_query, (slot_id, organizer_id))
    
    if not slot:
        return {"message": "Slot not found or unauthorized"}, 404


    # Bước 2: Kiểm tra ràng buộc (Optional)
    # Nếu đã có sinh viên đăng ký vào slot này thì có cho xóa không?
    # Tốt nhất là check trước.
    # app_check = "SELECT 1 FROM applications WHERE slot_id = %s LIMIT 1"
    # has_apps = db.fetch_one_sync(app_check, (slot_id,))
    # if has_apps:
    #     return {"message": "Cannot delete slot because students have already applied"}, 400
        
    try:
        # 2. Tự động REJECT các đơn đăng ký liên quan thay vì báo lỗi
        
        reject_query = """
            UPDATE applications
            SET 
                status = 'rejected',
                reason = 'Organizer cancelled this slot',
                decided_by = %s,
                decided_at = now(),
                updated_at = now()
            WHERE slot_id = %s -- Hủy các đơn về slot này đang treo
        """
        # Thực hiện update
        db.execute_query_sync(reject_query, (organizer_id, slot_id))

        # 3. Tiến hành xóa Slot
        delete_query = "DELETE FROM event_slots WHERE id = %s RETURNING id"
        result = db.fetch_one_sync(delete_query, (slot_id,))
        
        if result:
            return {"message": "Slot deleted and related applications were rejected"}, 200
        return {"message": "Failed to delete slot"}, 500

    except Exception as e:
        logger.error(f"Error deleting slot: {e}")
        return {"message": "Internal Server Error"}, 500

# 3. Cập nhật Slot
def update_slot(slot_id: str, request, organizer_id: str):
    # Bước 1: Check quyền sở hữu
    check_query = """
        SELECT s.id 
        FROM event_slots s
        JOIN events e ON e.id = s.event_id
        WHERE s.id = %s AND e.organizer_user_id = %s
    """
    slot = db.fetch_one_sync(check_query, (slot_id, organizer_id))
    if not slot:
        return {"message": "Slot not found or unauthorized"}, 404

    # Bước 2: Build câu query động (chỉ update cái nào gửi lên)
    fields = []
    params = []
    
    if request.work_date:
        fields.append("work_date = %s")
        params.append(request.work_date)
    if request.starts_at:
        fields.append("starts_at = %s")
        params.append(request.starts_at)
    if request.ends_at:
        fields.append("ends_at = %s")
        params.append(request.ends_at)
    if request.capacity is not None:
        fields.append("capacity = %s")
        params.append(request.capacity)
    if request.day_reward is not None:
        fields.append("day_reward = %s")
        params.append(request.day_reward)

    if not fields:
        return {"message": "No fields to update"}, 400

    params.append(slot_id)
    
    query = f"""
        UPDATE event_slots 
        SET {", ".join(fields)} 
        WHERE id = %s 
        RETURNING id, event_id, work_date, starts_at, ends_at, capacity, day_reward
    """
    
    updated_slot = db.fetch_one_sync(query, tuple(params))
    
    if updated_slot:
        return updated_slot, 200
    return {"message": "Update failed"}, 500

# 4. GET Slot Detail
def get_slot_detail(slot_id: str):
    # Query lấy thông tin Slot + Đếm số người
    query = """
        SELECT 
            s.id, 
            s.event_id, 
            s.work_date, 
            s.starts_at, 
            s.ends_at, 
            s.capacity, 
            s.day_reward,
            -- Đếm số người ĐÃ ĐƯỢC NHẬN (Approved)
            COUNT(a.student_user_id) FILTER (WHERE a.status IN ('approved')) AS approved_count,
            -- Đếm số người ĐANG CHỜ DUYỆT (Applied)
            COUNT(a.student_user_id) FILTER (WHERE a.status = 'applied') AS applied_count
        FROM event_slots s
        LEFT JOIN applications a ON s.id = a.slot_id -- Dùng LEFT JOIN để vẫn lấy được Slot dù chưa ai đăng ký
        WHERE s.id = %s
        GROUP BY s.id -- Group By(Count)
    """
    
    slot = db.fetch_one_sync(query, (slot_id,))
    
    if not slot:
        return None
    
    if slot.get('day_reward'):
        slot['day_reward'] = float(slot['day_reward'])
        
    return slot

def search_events(keyword: str):
    pattern = f"%{keyword}%"

    query = """ 
            SELECT
                e.id AS event_id,
                e.title AS event_name,
                o.org_name,
                e.description,
                e.location,
                e.status,
                s.id AS slot_id,
                s.event_id,
                s.work_date,
                s.starts_at,
                s.ends_at,
                s.capacity,
                s.day_reward,
                COALESCE(approved.approved_count, 0) AS approved_count,
                COALESCE(applied.applied_count, 0) AS applied_count
            FROM events e
            JOIN organizers o ON o.user_id = e.organizer_user_id
            LEFT JOIN event_slots s ON s.event_id = e.id

            -- Count số người applied + approved cho mỗi slot 
            LEFT JOIN (
                SELECT slot_id, COUNT(*) AS approved_count
                FROM applications
                WHERE status = 'approved'
                GROUP BY slot_id
            ) approved ON approved.slot_id = s.id

            LEFT JOIN (
                SELECT slot_id, COUNT(*) AS applied_count
                FROM applications
                WHERE status = 'applied'
                GROUP BY slot_id
            ) applied ON applied.slot_id = s.id

            WHERE 
                e.title ILIKE %s OR
                e.description ILIKE %s OR
                e.location ILIKE %s OR
                o.org_name ILIKE %s
            ORDER BY e.created_at DESC;
         """

    rows = db.execute_query_sync(query, (pattern, pattern, pattern, pattern))

    if not rows:
        return []

    # Group theo event_id
    events = {}

    for row in rows:
        event_id = row["event_id"]

        if event_id not in events:
            events[event_id] = {
                "event_id": event_id,
                "event_name": row["event_name"],
                "org_name": row["org_name"],
                "description": row["description"],
                "location": row["location"],
                "status": row["status"],
                "slots": []
            }

        # Nếu slot null (event chưa có slot)
        if row["slot_id"] is None:
            continue

        events[event_id]["slots"].append({
            "id": row["slot_id"],
            "event_id": row["event_id"],
            "work_date": row["work_date"],
            "starts_at": row["starts_at"],
            "ends_at": row["ends_at"],
            "capacity": row["capacity"],
            "day_reward": float(row["day_reward"]),
            "approved_count": row["approved_count"],
            "applied_count": row["applied_count"]
        })

    return list(events.values())

