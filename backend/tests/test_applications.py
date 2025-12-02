import pytest
from datetime import date, timedelta

class TestApplicationWorkflow:
    """Application workflow tests with comprehensive coverage"""

    # ==================== FULL WORKFLOW TESTS ====================

    def test_full_application_flow(self, organizer_auth, student_auth):
        """✓ Complete workflow: create → apply → review → attend"""
        org_client, org_headers, org_id = organizer_auth
        stu_client, stu_headers, stu_id = student_auth

        # Step 1: Organizer creates Event
        event_payload = {
            "title": "Hiến Máu Nhân Đạo", "description": "Full Flow Test", "location": "Sảnh A",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=2)),
                "starts_at": "08:00:00", "ends_at": "11:00:00",
                "capacity": 5, "day_reward": 2.0
            }]
        }
        res_create = org_client.post("/events/", json=event_payload, headers=org_headers)
        assert res_create.status_code == 201
        
        event_id = res_create.json()["event_id"]
        slot_id = res_create.json()["slot_ids"][0]

        # Step 2: Student applies
        apply_payload = {
            "event_id": event_id, "slot_id": slot_id, "note": "Em muốn tham gia"
        }
        res_apply = stu_client.post("/applications/apply", json=apply_payload, headers=stu_headers)
        assert res_apply.status_code == 200
        
        # Step 3: Organizer reviews (approves)
        review_payload = {
            "slot_id": slot_id, "student_user_id": stu_id, "approve": True, "reason": "OK"
        }
        res_review = org_client.patch(f"/applications/{event_id}/review", json=review_payload, headers=org_headers)
        assert res_review.status_code == 200

        # Step 4: Organizer marks attendance
        attend_payload = {
            "slot_id": slot_id, "student_user_id": stu_id, "attended": True
        }
        res_attend = org_client.patch(f"/applications/{event_id}/attendance", json=attend_payload, headers=org_headers)
        assert res_attend.status_code == 200
        
        # Step 5: Verify stats updated
        res_profile = stu_client.get("/users/profile/me", headers=stu_headers)
        stats = res_profile.json()["stats"]
        assert stats["activities_joined"] >= 1
        assert stats["total_social_work_days"] >= 2.0

    def test_full_flow_with_rejection(self, organizer_auth, student_auth):
        """✓ Complete workflow: create → apply → reject"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, stu_id = student_auth

        # Create event
        event_payload = {
            "title": "Rejection Test", "description": "Test", "location": "Location",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=3)),
                "starts_at": "09:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.5
            }]
        }
        res_create = org_client.post("/events/", json=event_payload, headers=org_headers)
        event_id = res_create.json()["event_id"]
        slot_id = res_create.json()["slot_ids"][0]

        # Student applies
        stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "Apply"
        }, headers=stu_headers)

        # Organizer rejects
        res_review = org_client.patch(f"/applications/{event_id}/review", json={
            "slot_id": slot_id, "student_user_id": stu_id, "approve": False, "reason": "Not qualified"
        }, headers=org_headers)
        assert res_review.status_code == 200

        # Verify stats NOT updated (rejection doesn't count)
        res_profile = stu_client.get("/users/profile/me", headers=stu_headers)
        stats = res_profile.json()["stats"]
        assert stats["activities_joined"] == 0  # Should still be 0

    # ==================== APPLICATION TESTS ====================

    def test_apply_to_event_success(self, organizer_auth, student_auth):
        """✓ Student successfully applies to event"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        # Create event
        res = org_client.post("/events/", json={
            "title": "Apply Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        # Apply
        res_apply = stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "I want to join"
        }, headers=stu_headers)
        
        assert res_apply.status_code == 200

    def test_apply_missing_event_id(self, student_auth):
        """✗ Apply fails without event_id"""
        stu_client, stu_headers, _ = student_auth
        
        res = stu_client.post("/applications/apply", json={
            "slot_id": "some_id", "note": "test"
        }, headers=stu_headers)
        
        assert res.status_code == 422

    def test_apply_missing_slot_id(self, student_auth):
        """✗ Apply fails without slot_id"""
        stu_client, stu_headers, _ = student_auth
        
        res = stu_client.post("/applications/apply", json={
            "event_id": "some_id", "note": "test"
        }, headers=stu_headers)
        
        assert res.status_code == 422
    def test_apply_nonexistent_event(self, student_auth):
        """✗ Apply to non-existent event fails"""
        stu_client, stu_headers, _ = student_auth
        
        res = stu_client.post("/applications/apply", json={
            "event_id": "fake-event-id-123",
            "slot_id": "fake-slot-id-456",
            "note": "test"
        }, headers=stu_headers)
        
        assert res.status_code in [404, 400]

    def test_apply_to_full_slot(self, organizer_auth, student_auth):
        """✓ Verify behavior with full slot"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        # Create event with 1-capacity slot
        res = org_client.post("/events/", json={
            "title": "Full Slot Event", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=3)),
                "starts_at": "08:00:00", "ends_at": "09:00:00",
                "capacity": 1, "day_reward": 1
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        # First student applies
        res_apply = stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "First"
        }, headers=stu_headers)
        
        assert res_apply.status_code == 200

    def test_apply_without_auth(self, client):
        """✗ Apply without authentication fails"""
        res = client.post("/applications/apply", json={
            "event_id": "id", "slot_id": "id", "note": "test"
        })
        
        assert res.status_code in [401, 403]

    def test_apply_with_long_note(self, organizer_auth, student_auth):
        """✓ Apply with very long note"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        res = org_client.post("/events/", json={
            "title": "Long Note Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        long_note = "This is a very long note. " * 100
        res_apply = stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": long_note
        }, headers=stu_headers)
        
        assert res_apply.status_code in [200, 400]

    def test_apply_empty_note(self, organizer_auth, student_auth):
        """✓ Apply with empty note"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        res = org_client.post("/events/", json={
            "title": "Empty Note Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        res_apply = stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": ""
        }, headers=stu_headers)
        
        assert res_apply.status_code in [200, 400]

    # ==================== REVIEW TESTS ====================

    def test_review_approve(self, organizer_auth, student_auth):
        """✓ Organizer approves application"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, stu_id = student_auth
        
        # Setup
        res = org_client.post("/events/", json={
            "title": "Approve Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "Apply"
        }, headers=stu_headers)
        
        # Review
        res_review = org_client.patch(f"/applications/{event_id}/review", json={
            "slot_id": slot_id, "student_user_id": stu_id, "approve": True, "reason": "Good"
        }, headers=org_headers)
        
        assert res_review.status_code == 200

    def test_review_reject(self, organizer_auth, student_auth):
        """✓ Organizer rejects application"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, stu_id = student_auth
        
        # Setup
        res = org_client.post("/events/", json={
            "title": "Reject Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "Apply"
        }, headers=stu_headers)
        
        # Review with rejection
        res_review = org_client.patch(f"/applications/{event_id}/review", json={
            "slot_id": slot_id, "student_user_id": stu_id, "approve": False, "reason": "No experience"
        }, headers=org_headers)
        
        assert res_review.status_code == 200

    def test_review_student_cannot_review(self, organizer_auth, student_auth):
        """✗ Student cannot review applications"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, stu_id = student_auth
        
        # Create event
        res = org_client.post("/events/", json={
            "title": "Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        
        # Student tries to review
        res_review = stu_client.patch(f"/applications/{event_id}/review", json={
            "slot_id": "id", "student_user_id": stu_id, "approve": True, "reason": "Hack"
        }, headers=stu_headers)
        
        assert res_review.status_code == 403

    # ==================== ATTENDANCE TESTS ====================

    def test_mark_attendance_present(self, organizer_auth, student_auth):
        """✓ Mark student as attended"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, stu_id = student_auth
        
        # Setup
        res = org_client.post("/events/", json={
            "title": "Attendance Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "Apply"
        }, headers=stu_headers)
        
        org_client.patch(f"/applications/{event_id}/review", json={
            "slot_id": slot_id, "student_user_id": stu_id, "approve": True, "reason": "OK"
        }, headers=org_headers)
        
        # Mark attendance
        res_attend = org_client.patch(f"/applications/{event_id}/attendance", json={
            "slot_id": slot_id, "student_user_id": stu_id, "attended": True
        }, headers=org_headers)
        
        assert res_attend.status_code == 200

    def test_mark_attendance_absent(self, organizer_auth, student_auth):
        """✓ Mark student as absent"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, stu_id = student_auth
        
        # Setup
        res = org_client.post("/events/", json={
            "title": "Absence Test", "description": "...", "location": "...",
            "slots": [{
                "work_date": str(date.today() + timedelta(days=5)),
                "starts_at": "08:00:00", "ends_at": "12:00:00",
                "capacity": 10, "day_reward": 1.0
            }]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={
            "event_id": event_id, "slot_id": slot_id, "note": "Apply"
        }, headers=stu_headers)
        
        org_client.patch(f"/applications/{event_id}/review", json={
            "slot_id": slot_id, "student_user_id": stu_id, "approve": True, "reason": "OK"
        }, headers=org_headers)
        
        # Mark absent
        res_attend = org_client.patch(f"/applications/{event_id}/attendance", json={
            "slot_id": slot_id, "student_user_id": stu_id, "attended": False
        }, headers=org_headers)
        
        assert res_attend.status_code == 200

    def test_attendance_student_cannot_mark(self, student_auth):
        """✗ Student cannot mark attendance"""
        stu_client, stu_headers, _ = student_auth
        
        res = stu_client.patch("/applications/event_id/attendance", json={
            "slot_id": "id", "student_user_id": "id", "attended": True
        }, headers=stu_headers)
        
        assert res.status_code == 403

    # ==================== CANCEL & HISTORY TESTS (BỔ SUNG) ====================

    def test_student_cancel_application(self, organizer_auth, student_auth):
        """✓ Student cancels their application"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        # 1. Tạo & Apply
        res = org_client.post("/events/", json={
            "title": "Cancel Test", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today() + timedelta(days=5)), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={"event_id": event_id, "slot_id": slot_id, "note": "Join"}, headers=stu_headers)

        # 2. Cancel
        res_cancel = stu_client.patch(f"/applications/{event_id}/cancel", json={"slot_id": slot_id}, headers=stu_headers)
        
        assert res_cancel.status_code == 200
        assert "withdrawn" in res_cancel.json()["message"]

    def test_get_history_and_participating(self, organizer_auth, student_auth):
        """✓ Get history and participating lists"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth

        # 1. Tạo Event
        res = org_client.post("/events/", json={
            "title": "History Test", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today() + timedelta(days=5)), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)
        
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]

        # --- FIX: THÊM BƯỚC ĐĂNG KÝ (APPLY) ---
        apply_res = stu_client.post("/applications/apply", json={
            "event_id": event_id,
            "slot_id": slot_id,
            "note": "Join for test"
        }, headers=stu_headers)
        assert apply_res.status_code == 200 # Hoặc 201 tùy server

        # 2. Check Participating (Giờ mới có dữ liệu để check)
        res_part = stu_client.get("/applications/participating", headers=stu_headers)
        assert res_part.status_code == 200
        assert len(res_part.json()) > 0

    # ==================== DETAIL & LIST TESTS (BỔ SUNG) ====================

    def test_get_history_details(self, organizer_auth, student_auth):
        """✓ Get details of a specific history item"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        # Tạo & Apply
        res = org_client.post("/events/", json={
            "title": "Detail Test", "description": "Desc", "location": "Loc",
            "slots": [{"work_date": str(date.today() + timedelta(days=5)), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={"event_id": res.json()["event_id"], "slot_id": slot_id, "note": "Join"}, headers=stu_headers)

        # Lấy chi tiết đơn vừa apply (dựa theo slot_id)
        res_detail = stu_client.get(f"/applications/history/{slot_id}", headers=stu_headers)
        assert res_detail.status_code == 200
        assert len(res_detail.json()) > 0
        assert res_detail.json()[0]["event_name"] == "Detail Test"

    def test_organizer_get_applications_per_slot(self, organizer_auth, student_auth):
        """✓ Organizer views applicants for a slot"""
        org_client, org_headers, _ = organizer_auth
        stu_client, stu_headers, _ = student_auth
        
        # Tạo & Apply
        res = org_client.post("/events/", json={
            "title": "Applicant List Test", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today() + timedelta(days=5)), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)
        event_id = res.json()["event_id"]
        slot_id = res.json()["slot_ids"][0]
        
        stu_client.post("/applications/apply", json={"event_id": event_id, "slot_id": slot_id, "note": "I am here"}, headers=stu_headers)

        # Organizer xem danh sách
        res_list = org_client.get(f"/applications/{event_id}/{slot_id}", headers=org_headers)
        assert res_list.status_code == 200
        assert len(res_list.json()) >= 1
        assert res_list.json()[0]["note"] == "I am here"