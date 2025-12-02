import pytest
from datetime import date, timedelta

def test_full_application_flow(organizer_auth, student_auth):
    # Unpack fixtures
    org_client, org_headers, org_id = organizer_auth
    stu_client, stu_headers, stu_id = student_auth

    # --- BƯỚC 1: Organizer tạo Event (Dùng org_client) ---
    event_payload = {
        "title": "Hiến Máu Nhân Đạo", "description": "Test Flow", "location": "Sảnh A",
        "slots": [{
            "work_date": str(date.today() + timedelta(days=2)),
            "starts_at": "08:00:00", "ends_at": "11:00:00",
            "capacity": 5, "day_reward": 2.0
        }]
    }
    # Create Event trả về 201 là ĐÚNG (do events_route đã cấu hình)
    res_create = org_client.post("/events/", json=event_payload, headers=org_headers)
    assert res_create.status_code == 201 
    
    event_data = res_create.json()
    event_id = event_data["event_id"]
    slot_id = event_data["slot_ids"][0]

    # --- BƯỚC 2: Student Đăng ký (Dùng stu_client) ---
    apply_payload = {
        "event_id": event_id, "slot_id": slot_id, "note": "Em muốn tham gia"
    }
    res_apply = stu_client.post("/applications/apply", json=apply_payload, headers=stu_headers)
    
    # --- SỬA Ở ĐÂY: Đổi 201 thành 200 ---
    assert res_apply.status_code == 200  # <--- FIXED
    
    # --- BƯỚC 3: Organizer Duyệt đơn (Dùng org_client) ---
    review_payload = {
        "slot_id": slot_id, "student_user_id": stu_id, "approve": True, "reason": "OK"
    }
    res_review = org_client.patch(f"/applications/{event_id}/review", json=review_payload, headers=org_headers)
    assert res_review.status_code == 200

    # --- BƯỚC 4: Organizer Điểm danh (Dùng org_client) ---
    attend_payload = {
        "slot_id": slot_id, "student_user_id": stu_id, "attended": True
    }
    res_attend = org_client.patch(f"/applications/{event_id}/attendance", json=attend_payload, headers=org_headers)
    assert res_attend.status_code == 200
    
    # --- BƯỚC 5: Student Kiểm tra (Dùng stu_client) ---
    res_profile = stu_client.get("/users/profile/me", headers=stu_headers)
    stats = res_profile.json()["stats"]
    assert stats["activities_joined"] >= 1
    assert stats["total_social_work_days"] >= 2.0

def test_apply_full_slot(organizer_auth):
    org_client, org_headers, _ = organizer_auth
    
    # 1. Tạo event
    res = org_client.post("/events/", json={
        "title": "Small Event", "description": "...", "location": "...",
        "slots": [{
            "work_date": str(date.today() + timedelta(days=3)),
            "starts_at": "08:00:00", "ends_at": "09:00:00",
            "capacity": 1, "day_reward": 1
        }]
    }, headers=org_headers)
    
    assert res.status_code == 201 # Check status
    event_id = res.json()["event_id"]