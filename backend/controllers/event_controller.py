from ..models.event_models import CreateEventRequest, UpdateEventRequest
from ..config.logger import logger
from ..db.database import db
from fastapi import Request
from ..dependencies import verify_csrf
# @app.get("/api/events")
def events(request: Request):
    verify_csrf(request)
    query = "SELECT id, title, description, start_time, end_time, location FROM events"
    events = db.execute_query_sync(query)
    if events:
        return {"events": events}, 200
    return {"message": "No events found"}, 404

# @app.post("/api/events")
def create_event(request: CreateEventRequest):
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
    verify_csrf(req)
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