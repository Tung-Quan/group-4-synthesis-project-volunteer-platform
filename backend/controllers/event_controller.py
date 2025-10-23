from ..models.event_models import *
from ..config.logger import logger
from ..db.database import db
from fastapi import Request
from ..config.security import assert_csrf
import json

# @app.get("/api/events")
def events(request: Request):
    assert_csrf(request)
    query = "SELECT id, title, description, start_time, end_time, location FROM events"
    events = db.execute_query_sync(query)
    if events:
        return {"events": events}, 200
    return {"message": "No events found"}, 404

# @app.post("/api/events")
def create_event(request: CreateEventRequest):
    check_role = f"""
        SELECT type FROM users WHERE id = '{request.organizer_id}'
    """
    user = db.execute_query(check_role)
    if not user or user[0]['type'] not in ("BOTH", "ORGANIZER"):
        return {"message": "You have no permission to this operation."}, 403
    
    query = f"""
    INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by)
    VALUES ('{request.title}', '{request.description}', '{request.location}', '{request.starts_at}', '{request.ends_at}', {request.capacity}, '{request.organizer_id}')
    RETURNING id;
    """
    event_id = db.execute_query(query)
    if event_id:
        return {"message": "Event created successfully", "event_id": event_id[0]['id']}, 201
    return {"message": "Failed to create event"}, 500

# @app.put("/api/events")
def update_event(request: UpdateEventRequest, req: Request):
    assert_csrf(req)
    query = "SELECT created_by FROM events WHERE id = %s"
    event = db.fetch_one_sync(query, (request.event_id,))
    if not event:
        return {"message": "Event not found"}, 404
    if event['created_by'] != request.organizer_id:
        return {"message": "Unauthorized"}, 403

    query = """UPDATE events
    SET title = %s,
        description = %s,
        location = %s,
        starts_at = %s,
        ends_at = %s,
        capacity = %s,
        updated_at = now()
    WHERE id = %s;"""

    success = db.execute_query_sync(query, (request.title, request.description, request.location, request.starts_at, request.ends_at, request.capacity, request.event_id))
    if success is not None:
        return {"message": "Event updated successfully"}, 200
    
    return {"message": "Failed to update event"}, 500

# @app.post("/api/apply_event")
def apply_event(request: ApplyEvent):
    check_query = f"""
        SELECT id FROM applications 
        WHERE event_id = '{request.event_id}' AND applicant_id = '{request.applicant_id}';
    """
    check_exist = db.execute_query(check_query)
    if check_exist and len(check_exist) > 0:
        return {"message": "You have already registered this event"}, 400
    
    slot_query = f"""
        SELECT capacity FROM events WHERE id = '{request.event_id}'
    """
    slot = db.execute_query(slot_query)
    if not slot:
        return {"message": "Event not found."}, 404
    capacity = slot[0][0]
    
    count_query = f"""
        SELECT COUNT(*) FROM applications
        WHERE event_id = '{request.event_id}'
    """
    count = db.execute_query(count_query)
    current = count[0][0] if count else 0

    if current >= capacity:
        return {"message": "Event slots are full. Failed registration."}, 400
    
    note_json = {
        "name": request.name,
        "department": request.department,
        "email": request.email,
        "phone_no": request.phone_no
    }
    note_str = json.dumps(note_json)

    register_query = f"""
        INSERT INTO applications (event_id, applicant_id, note)
        VALUES ('{request.event_id}', '{request.applicant_id}', '{note_str}')
        RETURNING id;
    """
    result = db.execute_query(register_query)
    if result:
        return {"message": "Success Registration!"}, 201
    return {"message": "Failed Registration. Please try again."}, 500

#@app.post("/api/review_application")
def review_application(request: ReviewApplication):
    check_role = f"SELECT type FROM users WHERE id = '{request.organizer_id}'"
    user = db.execute_query_sync(check_role)
    if not user or user[0]['type'] not in ("BOTH", "ORGANIZER"):
        return {"message": "You have no permission to this operation."}, 403
    
    query= f"""
        SELECT id, status, created_by AS organizer
        FROM applications a
        JOIN events e ON e.id = a.event_id
        WHERE a.id = '{request.application_id}';
    """
    app = db.execute_query_sync(query)

    app = app[0]
    if app["status"] not in ("PENDING",):
        return {"message": f"Application already {app['status']}."}, 400
    
    if app["organzier"] != request.organizer_id:
        return {"message": "You are not the organizer of this event."}, 403
    
    new_status = "APRROVED" if request.approve else "REJECTED"
    update_query = f"""
        UPDATE applications
        SET status = '{new_status}',
            reason = %s,
            decided_by = '{request.organizer_id}',
            decided_at = now()
        WHERE id = '{request.application_id}'
        RETURNING applicant_id;
    """
    result = db.execute_query_sync(update_query, (request.reason,))
    if not result:
        return {"message": "Failed to update the status of application."}
    return {"message": f"Application {new_status.lower()} successfully."}, 200

# @app.post("/api/check_attendance")
def check_attendance(request: CheckingAttendance):
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