from ..models.event_models import *
from ..config.logger import logger
from ..db.database import db
from fastapi import Request
from ..dependencies import verify_csrf
import json

def events():
    query = """SELECT id, title, description, starts_at, ends_at, capacity, location FROM events"""
    events = db.execute_query_sync(query)
    if not events:
        return None
    return events

def event_id(id: str):
    query = """
            SELECT id, title, description, starts_at, ends_at, capacity, location 
            FROM events
            WHERE id = %s
            """
    event = db.fetch_one_sync(query, (id,))
    if not event:
        return None
    return event

def create_event(request, organizer_id):
    params = list(request.model_dump().values()) # Convert the model into params without typing manually
    params.append(organizer_id)

    query = """
            INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
    event_id = db.execute_query_sync(query, tuple(params))

    if not event_id:
        return None
    return {"event_id":event_id[0]["id"]}

def update_event(request, organizer_id): #! Later check
    query = """
            SELECT created_by FROM events WHERE id = %s;
            """
    event = db.fetch_one_sync(query, (request.event_id,))
    if not event:
        return {"message": "Not Found"}, 404
    if event["created_by"] != organizer_id:
        return {"message": "Unauthorized"}, 401
    
    params = [request.title, request.description, request.location, request.starts_at, request.ends_at, request.capacity, request.event_id]

    update_query = """
        UPDATE events
        SET 
            title = %s,
            description = %s,
            location = %s,
            starts_at = %s,
            ends_at = %s,
            capacity = %s,
            updated_at = now()
        WHERE id = %s
        RETURNING id,
    """

    results = db.execute_query_sync(update_query, tuple(params))
    if not results:
        return {"message": "Failed to update event"}, 500
    return {"message":"Event updated successfully"}, 200

def apply_event(request, applicant_id):
    slot_query = """
                SELECT capacity
                FROM events
                WHERE id = %s
                """
    event = db.fetch_one_sync(slot_query, (request.event_id,))
    if not event:
        return {"message":"Event Not Found."}, 404
    
    params = [applicant_id, request.event_id]
    check_query = """
                SELECT id
                FROM applications
                WHERE event_id = %s AND application_id = %s
                """
    existing = db.fetch_one_sync(check_query, tuple(params))
    if existing:
        return {"message":"Already registered this event"}, 400
    
    count_query = """
                SELECT COUNT(*) AS current_count
                FROM applications
                WHERE event_id = %s
                """
    count_row = db.fetch_one_sync(count_query, (request.event_id,))
    current = count_row["current_count"] if count_row else 0
    capacity = event["capacity"]

    if current >= capacity:
        return {"message":"Full slot. Falied registration"}, 500
    
    note_json = {
        "name": request.name,
        "department": request.department,
        "email": request.email,
        "phone_no": request.phone_no
    }
    note_str = json.dumps(note_json)

    regis_params = [request.event_id, request.applicant_id, note_str]
    regis_query = """
                INSERT INTO applications (event_id, applicant_id, note)
                VALUES (%s, %s, %s)
                RETURNING id;
                """
    result = db.execute_query_sync(regis_query, tuple(regis_params))
    if not result:
        return {"message": "Failed registration. Please try again"}, 500
    return {"message": result[0]["id"]}, 201

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
    
def check_attendance(request):
    check_role = f"SELECT type FROM users WHERE id = '{request.organizer_id}'"
    user = db.execute_query(check_role)
    if not user or user[0][0] not in ("BOTH","ORGANIZER"):
        return {"message": "You are not allowed to do this operation."}, 403
    query = f"""
        UPDATE applications
        SET attendance = {str(request.attended).lower()}
        WHERE applicant_id = '{request.applicant_id}'
        RETURNING id;
    """

    result = db.execute_query(query)
    if result:
        return {"message": "Attendance updated!"}, 200
    return {"message": "Failed to update attendance."}, 500

def cancel_application(request: CancelApplication, applicant_id: str):
    query = """
        SELECT status
        FROM applications
        WHERE id = %s AND applicant_id = %s
    """
    app = db.fetch_one_sync(query, (request.application_id, applicant_id))
    if not app:
        return {"message": "Application not found"}, 404
    if app["status"] != "PENDING":
        return {"message": f"Cannot cancel an application that is {app['status']}"}, 400

    update_query = """
        UPDATE applications
        SET status = 'CANCELLED',
            decided_at = now(),
        WHERE id = %s
    """

    result = db.execute_query_sync(update_query, (request.application_id,))

    if not result:
        return {"message": "Failed to cancel application"}, 500

    return {"message": "Application cancelled successfully"}, 200
