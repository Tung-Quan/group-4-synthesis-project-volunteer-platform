from ..models.event_models import *
from ..config.logger import logger
from ..db.database import db
from fastapi import Request
from ..dependencies import verify_csrf
import json
from fastapi import HTTPException, status


def apply_event(request, student_user_id):
    # check_query = """
    #     SELECT event_id
    #     FROM applications
    #     WHERE event_id = %s AND student_user_id = %s AND slot_id = %s;
    # """
    # existing = db.fetch_one_sync(
    #     check_query, (request.event_id, student_user_id, request.slot_id))
    # if existing:
    #     return {"message": "Already registered for this event"}, 400

    check_query = """
        SELECT status
        FROM applications
        WHERE event_id = %s AND student_user_id = %s AND slot_id = %s;
    """
    existing = db.fetch_one_sync(
        check_query, (request.event_id, student_user_id, request.slot_id))

    # LOGIC MỚI Ở ĐÂY
    if existing:
        # Nếu đã tồn tại nhưng trạng thái là withdrawn hoặc rejected, cho phép cập nhật lại thành applied
        if existing['status'] in ('withdrawn', 'rejected'):
            reactivate_query = """
                UPDATE applications
                SET status = 'applied', note = %s, updated_at = now()
                WHERE event_id = %s AND student_user_id = %s AND slot_id = %s
                RETURNING event_id;
            """
            result = db.execute_query_sync(
                reactivate_query, (request.note, request.event_id, student_user_id, request.slot_id))
            if result:
                return {"message": "Successfully re-registered!"}, 201
            else:
                return {"message": "Failed to re-register."}, 500
        else:
            return {"message": "Already registered for this event"}, 400

    slot_query = """
        SELECT capacity
        FROM event_slots
        WHERE id = %s AND event_id = %s;
    """
    slot = db.fetch_one_sync(slot_query, (request.slot_id, request.event_id))
    if not slot:
        return {"message": "Slot not found"}, 404

    capacity = slot["capacity"]

    count_query = """
        SELECT COUNT(*) AS current_count
        FROM applications
        WHERE event_id = %s AND slot_id = %s;
    """
    count_row = db.fetch_one_sync(
        count_query, (request.event_id, request.slot_id))
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

def review_application(event_id, request, organizer_id):
    app_query = """
        SELECT 
            a.event_id,
            a.slot_id,
            a.student_user_id,
            a.status,
            e.organizer_user_id
        FROM applications a
        JOIN events e ON e.id = a.event_id
        WHERE a.event_id = %s 
          AND a.slot_id = %s
          AND a.student_user_id = %s
    """

    app = db.fetch_one_sync(app_query, (
        event_id,
        request.slot_id,
        request.student_user_id
    ))

    if not app:
        return {"message": "Application not found"}, 404

    if app["status"] != "applied":
        return {
            "message": f"Application already '{app['status']}'"
        }, 400

    if app["organizer_user_id"] != organizer_id:
        return {"message": "Unauthorized"}, 401

    new_status = "approved" if request.approve else "rejected"

    update_query = """
        UPDATE applications
        SET 
            status = %s,
            reason = %s,
            decided_by = %s,
            decided_at = now(),
            updated_at = now()
        WHERE event_id = %s
          AND slot_id = %s
          AND student_user_id = %s
        RETURNING event_id, slot_id, student_user_id;
    """

    result = db.execute_query_sync(update_query, (
        new_status,
        request.reason,
        organizer_id,
        event_id,
        request.slot_id,
        request.student_user_id
    ))

    if not result:
        return {"message": "Failed to update application status"}, 500

    return {
        "message": f"Application {new_status} successfully"
    }, 200


def mark_attendance(event_id, request, organizer_id: str):
    event_query = """
        SELECT organizer_user_id
        FROM events
        WHERE id = %s
    """
    event = db.fetch_one_sync(event_query, (event_id,))

    if not event:
        return {"message": "Event not found"}, 404

    if event["organizer_user_id"] != organizer_id:
        return {"message": "Unauthorized"}, 403

    app_query = """
        SELECT status
        FROM applications
        WHERE event_id = %s AND slot_id = %s AND student_user_id = %s
    """
    app = db.fetch_one_sync(app_query, (
        event_id,
        request.slot_id,
        request.student_user_id
    ))

    if not app:
        return {"message": "Application not found"}, 404

    if app["status"] != "approved":
        return {
            "message": f"Cannot mark attendance for an application that is '{app['status']}'"
        }, 400

    new_status = "attended" if request.attended else "absent"

    update_query = """
        UPDATE applications
        SET 
            status = %s,
            decided_by = %s,
            decided_at = now(),
            updated_at = now()
        WHERE event_id = %s AND slot_id = %s AND student_user_id = %s
        RETURNING event_id;
    """

    params = (
        new_status,
        organizer_id,
        event_id,
        request.slot_id,
        request.student_user_id,
    )

    result = db.execute_query_sync(update_query, params)

    if not result:
        return {"message": "Failed to update attendance"}, 500

    return {"message": f"Marked as {new_status}"}, 200


def cancel_application(event_id, request, student_user_id: str):
    query = """
        SELECT status
        FROM applications
        WHERE event_id = %s AND student_user_id = %s AND slot_id = %s;
    """
    app = db.fetch_one_sync(
        query, (event_id, student_user_id, request.slot_id))

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
        WHERE event_id = %s AND student_user_id = %s AND slot_id = %s
        RETURNING event_id, student_user_id;
    """

    result = db.execute_query_sync(
        update_query, (event_id, student_user_id, request.slot_id))

    if not result:
        return {"message": "Failed to cancel application"}, 500

    return {"message": "Application withdrawn successfully"}, 200


def get_history(student_user_id):
    query = """
        SELECT
            a.event_id,
            a.slot_id,       
            e.title AS event_name,
            s.work_date,
            s.starts_at,
            s.ends_at,
            e.location,
            a.status
        FROM applications a
        JOIN events e ON e.id = a.event_id
        LEFT JOIN event_slots s ON s.id = a.slot_id
        WHERE a.student_user_id = %s
        AND a.status IN ('attended')
        ORDER BY s.work_date DESC;
        """
    results = db.execute_query_sync(query, (student_user_id,))
    if not results:
        return None
    return results


def get_participating(student_user_id):
    query = """
        SELECT
            a.event_id,
            a.slot_id,      
            e.title AS event_name,
            s.work_date,
            s.starts_at,
            s.ends_at,
            e.location,
            a.status
        FROM applications a
        JOIN events e ON e.id = a.event_id
        LEFT JOIN event_slots s ON s.id = a.slot_id
        WHERE a.student_user_id = %s
        AND (a.status = 'approved' OR a.status = 'applied')
        ORDER BY s.work_date DESC;
        """
    results = db.execute_query_sync(query, (student_user_id,))
    if not results:
        return None
    return results


def get_application_details(slot_id, student_user_id):
    query = """
        SELECT
            a.event_id,
            e.title AS event_name,
            o.org_name AS org_name,
            e.description,
            s.work_date,
            s.starts_at,
            s.ends_at,
            e.location,
            s.day_reward,
            a.status
        FROM applications a
        JOIN events e ON e.id = a.event_id
        LEFT JOIN event_slots s ON s.id = a.slot_id
        JOIN organizers o ON o.user_id = e.organizer_user_id
        WHERE a.slot_id = %s AND a.student_user_id = %s
        ORDER BY s.work_date DESC;
    """
    results = db.execute_query_sync(query, (slot_id, student_user_id))
    if not results:
        return None
    return results

def get_application_by_slotId(event_id, slot_id):
    check_exist = """
        SELECT id, event_id
        FROM event_slots
        WHERE event_id = %s AND id = %s;
        """
    rows = db.execute_query_sync(check_exist, (event_id, slot_id))
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    query = """
        SELECT
            u.full_name AS student_name,
            s.student_no,
            a.note,
            a.status
        FROM applications a
        JOIN users u ON a.student_user_id = u.id
        JOIN students s ON a.student_user_id = s.user_id
        WHERE a.event_id = %s AND a.slot_id = %s;
        """
    
    results = db.execute_query_sync(query, (event_id, slot_id))
    if not results:
        return []
    return results
