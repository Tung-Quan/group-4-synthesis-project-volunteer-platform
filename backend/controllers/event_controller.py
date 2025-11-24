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

def apply_event(request, student_user_id):
    slot_query = """
        SELECT capacity
        FROM event_slots
        WHERE id = %s AND event_id = %s
    """
    slot = db.fetch_one_sync(slot_query, (request.slot_id, request.event_id))
    if not slot:
        return {"message": "Slot not found"}, 404

    capacity = slot["capacity"]

    check_query = """
        SELECT event_id
        FROM applications
        WHERE event_id = %s AND student_user_id = %s
    """
    existing = db.fetch_one_sync(check_query, (request.event_id, student_user_id))
    if existing:
        return {"message": "Already registered for this event"}, 400

    count_query = """
        SELECT COUNT(*) AS current_count
        FROM applications
        WHERE slot_id = %s
    """
    count_row = db.fetch_one_sync(count_query, (request.slot_id,))
    current = count_row["current_count"] if count_row else 0

    if current >= capacity:
        return {"message": "Slot is full. Registration failed"}, 400

    insert_query = """
        INSERT INTO applications (event_id, student_user_id, slot_id, note)
        VALUES (%s, %s, %s, %s)
        RETURNING event_id, student_user_id;
    """

    params = (
        request.event_id,
        student_user_id,
        request.slot_id,
        request.note
    )

    result = db.execute_query_sync(insert_query, params)
    if not result:
        return {"message": "Failed registration. Please try again"}, 500

    return {"message": "Successfully registered!"}, 201

def review_application(request, organizer_id):
    app_query = """
                SELECT 
                a.id AS application_id,
                a.status,
                e.created_by AS event_organizer
                FROM applications a
                JOIN events e ON e.id = a.event_id
                WHERE a.id = %s
                """
    app = db.fetch_one_sync(app_query, (request.application_id,))
    if not app:
        return {"message": "Application Not Found"}, 404
    if app["status"] != "PENDING":
        return {"message": "Application has already been approved"}, 400
    if app["event_organizer"] != organizer_id:
        return {"message": "Unauthorized"}, 401
    
    new_status = "APPROVED" if request.approve else "REJECTED"

    update_query = """
                UPDATE applications
                SET 
                    status = %s,
                    reason = %s,
                    decided_by = %s,
                    decided_at = now()
                WHERE id = %s
                """
    update_params = [new_status, request.reason, organizer_id, request.application_id]
    result = db.execute_query_sync(update_query, tuple(update_params))
    if not result:
        return {"message": "Failed to update application status"}, 500
    return {"message": f"Application {new_status} successfully"}, 200
    
# def check_attendance(request):
#     check_role = f"SELECT type FROM users WHERE id = '{request.organizer_id}'"
#     user = db.execute_query(check_role)
#     if not user or user[0][0] not in ("BOTH","ORGANIZER"):
#         return {"message": "You are not allowed to do this operation."}, 403
#     query = f"""
#         UPDATE applications
#         SET attendance = {str(request.attended).lower()}
#         WHERE applicant_id = '{request.applicant_id}'
#         RETURNING id;
#     """

#     result = db.execute_query(query)
#     if result:
#         return {"message": "Attendance updated!"}, 200
#     return {"message": "Failed to update attendance."}, 500

def cancel_application(request, student_user_id: str):
    query = """
        SELECT status
        FROM applications
        WHERE event_id = %s AND student_user_id = %s
    """
    app = db.fetch_one_sync(query, (request.event_id, student_user_id))

    if not app:
        return {"message": "Application not found"}, 404

    if app["status"] != "applied":
        return {
            "message": f"Cannot cancel an application that is '{app['status']}'"
        }, 400

    update_query = """
        UPDATE applications
        SET 
            status = 'withdrawn',
            updated_at = now()
        WHERE event_id = %s AND student_user_id = %s
        RETURNING event_id, student_user_id;
    """

    result = db.execute_query_sync(update_query, (request.event_id, student_user_id))

    if not result:
        return {"message": "Failed to cancel application"}, 500

    return {"message": "Application withdrawn successfully"}, 200

